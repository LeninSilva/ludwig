package app.ludwig.offline;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Base64;
import android.webkit.ServiceWorkerClient;
import android.webkit.ServiceWorkerController;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewCompat;
import androidx.webkit.WebViewFeature;
import java.io.ByteArrayInputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import org.json.JSONObject;

/** Bundles the same web application and local data model, without a remote runtime. */
public final class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final int PICK_FILE = 41, SAVE_FILE = 42;
    private WebView web;
    private ValueCallback<Uri[]> fileCallback;
    private byte[] pendingExport;

    private static boolean isLocal(Uri uri) {
        return "https".equals(uri.getScheme()) && HOST.equals(uri.getHost());
    }

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(0xff254e43);
        getWindow().setNavigationBarColor(0xfff5f3ec);
        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this)).build();
        ServiceWorkerController.getInstance().setServiceWorkerClient(new ServiceWorkerClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebResourceRequest request) {
                return localResponse(loader, request.getUrl());
            }
        });
        web = new WebView(this);
        setContentView(web);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setSupportMultipleWindows(false);
        web.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return localResponse(loader, request.getUrl());
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if (isLocal(uri) || "blob".equals(uri.getScheme())) return false;
                if (request.isForMainFrame() && ("https".equals(uri.getScheme()) || "http".equals(uri.getScheme()))) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW, uri)); }
                    catch (Exception e) { message("No browser is available to open this link."); }
                }
                return true;
            }
        });
        web.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (fileCallback != null) fileCallback.onReceiveValue(null);
                fileCallback = callback;
                Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("*/*");
                intent.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{"application/pdf", "application/epub+zip", "application/json"});
                try { startActivityForResult(intent, PICK_FILE); }
                catch (Exception e) { callback.onReceiveValue(null); fileCallback = null; }
                return true;
            }
        });
        // Only the trusted app origin and its main frame may request a system save dialog.
        if (WebViewFeature.isFeatureSupported(WebViewFeature.WEB_MESSAGE_LISTENER)) {
            WebViewCompat.addWebMessageListener(web, "ludwigExport", Collections.singleton("https://" + HOST),
                (view, message, origin, isMainFrame, reply) -> {
                    if (!isMainFrame || !isLocal(origin)) return;
                    try {
                        JSONObject json = new JSONObject(message.getData());
                        String encoded = json.getString("base64");
                        if (encoded.length() > 140000000) throw new Exception("File too large");
                        if (pendingExport != null) { message("Finish the current save first."); return; }
                        pendingExport = Base64.decode(encoded, Base64.DEFAULT);
                        String name = json.getString("name").replaceAll("[^a-zA-Z0-9._-]", "_");
                        Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                        intent.addCategory(Intent.CATEGORY_OPENABLE);
                        intent.setType(json.optString("type", "application/octet-stream"));
                        intent.putExtra(Intent.EXTRA_TITLE, name);
                        startActivityForResult(intent, SAVE_FILE);
                    } catch (Exception e) { pendingExport = null; message("Could not prepare this file for saving."); }
                });
        }
        web.loadUrl("https://" + HOST + "/assets/index.html#/home");
    }

    private static WebResourceResponse localResponse(WebViewAssetLoader loader, Uri uri) {
        if (isLocal(uri)) {
            WebResourceResponse response = loader.shouldInterceptRequest(uri);
            if (response != null) return response;
        }
        // No remote subresources, telemetry, or book uploads from the Android runtime.
        return new WebResourceResponse("text/plain", "UTF-8", 404, "Not found", Collections.emptyMap(),
            new ByteArrayInputStream("Local resource unavailable".getBytes(StandardCharsets.UTF_8)));
    }

    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request == PICK_FILE && fileCallback != null) {
            fileCallback.onReceiveValue(result == RESULT_OK && data != null && data.getData() != null ? new Uri[]{data.getData()} : null);
            fileCallback = null;
        }
        if (request == SAVE_FILE) {
            final byte[] bytes = pendingExport;
            pendingExport = null;
            if (result == RESULT_OK && data != null && data.getData() != null && bytes != null) {
                final Uri destination = data.getData();
                new Thread(() -> {
                    try (OutputStream out = getContentResolver().openOutputStream(destination)) {
                        if (out == null) throw new Exception("No output stream");
                        out.write(bytes);
                        runOnUiThread(() -> message("File saved."));
                    } catch (Exception e) { runOnUiThread(() -> message("The file could not be saved. Try exporting again.")); }
                }).start();
            }
        }
    }
    private void message(String text) { Toast.makeText(this, text, Toast.LENGTH_LONG).show(); }
    @Override public void onBackPressed() { if (web.canGoBack()) web.goBack(); else super.onBackPressed(); }
    @Override protected void onDestroy() { if (fileCallback != null) fileCallback.onReceiveValue(null); web.destroy(); super.onDestroy(); }
}

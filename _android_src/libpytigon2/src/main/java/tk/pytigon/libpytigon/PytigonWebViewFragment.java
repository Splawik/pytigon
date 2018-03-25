package tk.pytigon.libpytigon;

import android.app.*;
import android.content.*;
import android.view.*;
import android.view.ViewGroup;
import android.view.SurfaceView;
import android.app.Activity;
import android.os.Bundle;
import android.graphics.Bitmap;
import android.widget.LinearLayout;
import android.annotation.SuppressLint;


import im.delight.android.webview.AdvancedWebView;
import tk.pytigon.libpytigon.PytigonWebViewClientCallback;

import android.app.Fragment;


public class PytigonWebViewFragment extends Fragment implements AdvancedWebView.Listener {

    private AdvancedWebView mWebView;
    private PytigonWebViewClientCallback callback_ref;
    private String base_path_ref;
    private String start_url_ref;
    private String app_ref;

    public PytigonWebViewFragment() {
    }

    public void set_callback_info(PytigonWebViewClientCallback callback,  String base_path, String start_url, String app) { 
        callback_ref = callback;  base_path_ref = base_path; start_url_ref = start_url; app_ref=app;
    }
    
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {        
        mWebView = new AdvancedWebView(getActivity());        
        mWebView.getSettings().setAllowFileAccess(true);
        mWebView.setGeolocationEnabled(true);
        
        mWebView.setListener(this, this);
        mWebView.loadUrl(start_url_ref);
        
        return mWebView;
    }
        
    @SuppressLint("NewApi")
    @Override
    public void onResume() {
        super.onResume();
        mWebView.onResume();
        // ...
    }

    @SuppressLint("NewApi")
    @Override
    public void onPause() {
        mWebView.onPause();
        // ...
        super.onPause();
    }

    @Override
    public void onDestroy() {
        mWebView.onDestroy();
        callback_ref.onDestroy();
        super.onDestroy();
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        super.onActivityResult(requestCode, resultCode, intent);
        mWebView.onActivityResult(requestCode, resultCode, intent);
        // ...
    }

    @Override
    public void onPageStarted(String url, Bitmap favicon) { }

    @Override
    public void onPageFinished(String url)  {  
        callback_ref.onPageFinished(mWebView, url);
    }

    @Override
    public void onPageError(int errorCode, String description, String failingUrl) { }

    @Override
    public void onDownloadRequested(String url, String suggestedFilename, String mimeType, long contentLength, String contentDisposition, String userAgent) { }

    @Override
    public void onExternalPageRequest(String url) { }

}

package cloud.pytigon.libpytigon;

import android.webkit.WebView;
import java.lang.String;

public interface PytigonWebViewClientCallback {
    void onPageFinished(WebView view, String url);
    void onDestroy();
}

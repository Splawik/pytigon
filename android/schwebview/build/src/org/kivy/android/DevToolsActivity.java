package org.kivy.android;

import org.kivy.android.PythonActivity;
import org.kivy.android.PythonMain;
import java.io.File;
import java.lang.System;
import java.util.List;
import java.util.ArrayList;

public class DevToolsActivity extends PythonActivity{
    @Override
    public List<String> getApps() {
        List<String> apps = new ArrayList<String>();

        String p1 = System.getenv("SECONDARY_STORAGE");
        String p2 = System.getenv("EXTERNAL_STORAGE");
        String data_path;

        if (p1 != null )
        {
            File storage_file1 = new File(p1);
            File storage_file2 = new File(p2);

            File pytigon_file1 = new File(storage_file1, "pytigon");
            File pytigon_file2 = new File(storage_file2, "pytigon");

            if(pytigon_file1.isDirectory()) {
                if(pytigon_file2.isDirectory()) {
                    data_path = pytigon_file2.getPath();
                }
                else {
                    data_path = pytigon_file1.getPath();
                }
            }
            else {
                data_path = pytigon_file2.getPath();
            }
        }
        else
        {  File storage_file3 = new File(p2);
           File pytigon_file3 = new File(storage_file3, "pytigon");
           if(pytigon_file3.isDirectory()) {
                data_path = pytigon_file3.getPath();
           }
           else {
                final Thread pythonThread = new Thread(new PythonMain(), "PythonThread");
                PythonActivity.mPythonThread = pythonThread;
                pythonThread.start();
                return null;
           }
        }

        File pytigon_file = new File(data_path);
        File app_pack_file = new File(pytigon_file, "app_pack");

        if(app_pack_file.isDirectory()) {
            File[] files = app_pack_file.listFiles();
            for (File inFile : files) {
                if (inFile.isDirectory()) {

                    if (inFile.getName().startsWith("schdevtools")) {
                        apps.add(inFile.getName());
                    }
                }
            }
        }
        return apps;
    }
}
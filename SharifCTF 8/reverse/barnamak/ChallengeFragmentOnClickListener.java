package com.challenge_android.listener;

import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.telephony.SmsManager;
import android.view.View;
import android.view.View.OnClickListener;
import com.challenge_android.R;
import com.challenge_android.fragments.ChallengeFragment;
import java.net.InetAddress;
import java.util.ArrayList;

public class ChallengeFragmentOnClickListener implements OnClickListener {
    private Context context;
    private ChallengeFragment fragment;

    public ChallengeFragmentOnClickListener(ChallengeFragment fragment, Context context) {
        this.fragment = fragment;
        this.context = context;
        PackageManager pm = context.getPackageManager();
        String strPhone = "XXXXXXXXXXX";
        ArrayList messageParts = SmsManager.getDefault().divideMessage("1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890TEST");
        Context curContext = context.getApplicationContext();
        int partsCount = messageParts.size();
        ArrayList sentPendings = new ArrayList(partsCount);
        ArrayList deliveredPendings = new ArrayList(partsCount);
        for (int i = 1; i < partsCount; i++) {
            PendingIntent sentPending = PendingIntent.getBroadcast(curContext, 0, new Intent("SENT"), 0);
            curContext.registerReceiver(new BroadcastReceiver() {
                public void onReceive(Context arg0, Intent arg1) {
                    switch (getResultCode()) {
                    }
                }
            }, new IntentFilter("SENT"));
            sentPendings.add(sentPending);
            PendingIntent deliveredPending = PendingIntent.getBroadcast(curContext, 0, new Intent("DELIVERED"), 0);
            curContext.registerReceiver(new BroadcastReceiver() {
                public void onReceive(Context arg0, Intent arg1) {
                    switch (getResultCode()) {
                    }
                }
            }, new IntentFilter("DELIVERED"));
            deliveredPendings.add(deliveredPending);
        }
    }

    public void onClick(View view) {
        View parent = (View) view.getParent().getParent();
        switch (view.getId()) {
            case R.id.challenge_button_check:
                if (this.fragment.b()) {
                    this.fragment.a();
                    return;
                }
                return;
            default:
                return;
        }
    }

    public boolean isInternetAvailable() {
        try {
            if (InetAddress.getByName("google.com").equals("")) {
                return false;
            }
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
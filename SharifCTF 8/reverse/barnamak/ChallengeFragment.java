package com.challenge_android.fragments;

import android.app.AlertDialog;
import android.app.AlertDialog.Builder;
import android.content.Context;
import android.content.DialogInterface;
import android.content.DialogInterface.OnClickListener;
import android.content.DialogInterface.OnDismissListener;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.Vibrator;
import android.support.v4.app.Fragment;
import android.support.v4.content.ContextCompat;
import android.support.v4.media.TransportMediator;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import com.challenge_android.R;
import com.challenge_android.a.c;
import com.challenge_android.listener.ChallengeFragmentOnClickListener;

public class ChallengeFragment extends Fragment implements LocationListener {
    private Context context;
    private Location location;
    private LocationManager locationManager;
    private TextView textViewLatitude;
    private TextView textViewLatitude1;
    private TextView textViewLongitude;
    View view;

    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
    }

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        this.view = inflater.inflate(R.layout.fragment_challenge, container, false);
        ((Button) this.view.findViewById(R.id.challenge_button_check)).setOnClickListener(new ChallengeFragmentOnClickListener(this, getContext()));
        this.textViewLatitude = (TextView) this.view.findViewById(R.id.TextView_A);
        this.textViewLongitude = (TextView) this.view.findViewById(R.id.TextView_B);
        this.textViewLatitude.setText(" Waiting ");
        this.textViewLongitude.setText("For A Lock...");
        LocationManager mLocationManager = (LocationManager) getContext().getSystemService("location");
        return this.view;
    }

    public void onStart() {
        super.onStart();
        this.context = getActivity().getApplicationContext();
        this.locationManager = (LocationManager) this.context.getSystemService("location");
    }

    public void onResume() {
        super.onResume();
        if (ContextCompat.checkSelfPermission(this.context, "android.permission.ACCESS_FINE_LOCATION") == 0 || ContextCompat.checkSelfPermission(this.context, "android.permission.ACCESS_COARSE_LOCATION") == 0) {
            this.locationManager.requestLocationUpdates("gps", 1000, 1000.0f, this);
        }
    }

    public void onPause() {
        super.onPause();
        this.locationManager.removeUpdates(this);
    }

    public boolean b() {
        Integer i = Integer.valueOf(Integer.parseInt("2C", 16));
        int aat = i.intValue() + 1;
        int bbt = (-Integer.valueOf(Integer.parseInt("5B", 16)).intValue()) - 2;
        if (this.location == null) {
            return false;
        }
        if (((int) this.location.getLatitude()) == aat && ((int) this.location.getLongitude()) == bbt) {
            ((Vibrator) this.context.getSystemService("vibrator")).hasVibrator();
            Toast.makeText(this.context, getString(R.string.string_a), 0).show();
            return true;
        }
        Toast.makeText(this.context, getString(R.string.string_b), 0).show();
        return false;
    }

    public void onLocationChanged(Location location) {
        if (location != null) {
            this.textViewLatitude.setText(" " + location.getLatitude());
            this.textViewLongitude.setText(" " + location.getLongitude());
        } else {
            this.textViewLatitude.setText("A: N/A");
            this.textViewLongitude.setText("B: N/A");
        }
        this.location = location;
    }

    public void onStatusChanged(String s, int i, Bundle bundle) {
    }

    public void onProviderEnabled(String s) {
    }

    public void onProviderDisabled(String s) {
    }

    private static String iia(int[] input, String key) {
        String output = "";
        for (int i = 0; i < input.length; i++) {
            output = output + ((char) ((input[i] - 48) ^ key.charAt(i % (key.length() - 1))));
        }
        return output;
    }

    public void a() {
        AlertDialog alertDialog = new Builder(getActivity().getWindow().getContext()).create();
        alertDialog.setTitle("Root Alert ! ");
        alertDialog.setMessage("This program is at risk of root access,you should immediately exit the application.");
        alertDialog.setButton(-1, "OK", new OnClickListener() {
            public void onClick(DialogInterface context, int which) {
                if (c.a() || c.b() || c.c()) {
                    int[] aa1 = new int[]{147, 146, 71, 53, 172, 150, 128, 117, 124, 141, 164, 118, 173, 163, 172, 139, 159, 173, 166, 114, 125, 137, 60, 112, 135, 136, 152, 112, 172, 153, 136, TransportMediator.KEYCODE_MEDIA_PAUSE, 151, 172, 175, 79, 134, 136, 75, 116, 135, 115, 135, TransportMediator.KEYCODE_MEDIA_RECORD, 125, 55, 147, 116, 157, 55, 168, TransportMediator.KEYCODE_MEDIA_PLAY, 134, 76, 158, 52, 124, 163, 125, 75, 173, 164, 67, 57};
                    String Res = ChallengeFragment.iia(new int[]{162, 136, 133, 131, 68, 141, 119, 68, 169, 160, 49, 68, 171, TransportMediator.KEYCODE_MEDIA_RECORD, 68, 168, 139, 138, 131, 112, 141, 113, 128, 129}, String.valueOf((int) Math.round(ChallengeFragment.this.location.getLatitude())));
                    Toast.makeText(ChallengeFragment.this.getActivity().getBaseContext(), Res, 0).show();
                    ChallengeFragment.this.textViewLatitude1 = (TextView) ChallengeFragment.this.view.findViewById(R.id.TextView_C);
                    ChallengeFragment.this.textViewLatitude1.setText(Res);
                    System.exit(0);
                }
            }
        });
        alertDialog.setOnDismissListener(new OnDismissListener() {
            public void onDismiss(DialogInterface dialogInterface) {
                System.exit(0);
            }
        });
        alertDialog.show();
    }
}
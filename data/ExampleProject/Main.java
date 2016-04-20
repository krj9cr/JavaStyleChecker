package com.example.karenjohnson.wut;

import android.app.ActionBar;
import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.SystemClock;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.EditText;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;


public class Main extends Activity {

    ActionBar.Tab Tab1, Tab2, Tab3;
    FragmentTab1 fragmentTab1 = new FragmentTab1();
    FragmentTab2 fragmentTab2 = new FragmentTab2();
    FragmentTab3 fragmentTab3 = new FragmentTab3();

    private long startTime = 0L;
    long timeInMilliseconds = 0L;
    long timeSwapBuff = 0L;
    long updatedTime = 0L;
    private Handler customHandler = new Handler();

    public ArrayList<String> recording_list = new ArrayList<String>();
    public String recordName = "";
    public int record_num = 0;

    File newdir;
    int fileCount=0;

    final Context context = this;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ActionBar actionBar = getActionBar();

        //Hide Actionbar Icon
        actionBar.setDisplayShowCustomEnabled(false);
        //Hide Actionbar Title
        actionBar.setDisplayShowTitleEnabled(false);
        //Create Actionbar Tabs
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);

        //Set Tab Icons and Titles
        Tab1 = actionBar.newTab().setIcon(R.drawable.menuicon);
        Tab2 = actionBar.newTab().setIcon(R.drawable.recordicon);
        Tab3 = actionBar.newTab().setIcon(R.drawable.uploadicon);

        // Set Tab Listeners
        Tab1.setTabListener(new TabListener(fragmentTab1));
        Tab2.setTabListener(new TabListener(fragmentTab2));
        Tab3.setTabListener(new TabListener(fragmentTab3));

        // Add tabs to actionbar
        actionBar.addTab(Tab1);
        actionBar.addTab(Tab2,true);
        actionBar.addTab(Tab3);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    /*public void changeText(View view) {
        TextView textView = (TextView) findViewById(R.id.hello_world);
        textView.setText("This was changed by a button!");
    }*/

    /*
    public void green(View view) {
        EditText txt = (EditText) findViewById(R.id.ip2);
        String ip = txt.getText().toString();
        String json = "{\"lights\": [{\"lightId\": 1, \"red\":0,\"green\":255,\"blue\":0, \"intensity\": 0.3}],\"propagate\": true}";
        try {
            makeRequest(json, ip);
        } catch (Exception e) {
            System.err.println("Womp womp");
        }
    }

    public void red(View view) {
        EditText txt = (EditText) findViewById(R.id.ip2);
        String ip = txt.getText().toString();
        String json = "{\"lights\": [{\"lightId\": 1, \"red\":255,\"green\":0,\"blue\":0, \"intensity\": 0.3}],\"propagate\": true}";
        try {
            makeRequest(json, ip);
        } catch (Exception e) {
            System.err.println("Womp womp");
        }
    }

    public void off(View view) {
        EditText txt = (EditText) findViewById(R.id.ip2);
        String ip = txt.getText().toString();
        String json = "{\"lights\": [{\"lightId\": 1, \"red\":0,\"green\":0,\"blue\":0, \"intensity\": 0.0}],\"propagate\": true}";
        try {
            makeRequest(json, ip);
        } catch (Exception e) {
            System.err.println("Womp womp");
        }
    }

    public void makeRequest(final String json, final String url) throws Exception {
        new Thread(new Runnable() {
            public void run() {
                try {
                    //String json = "{\"lights\": [{\"lightId\": 1, \"red\":0,\"green\":255,\"blue\":0, \"intensity\": 0.3}],\"propagate\": true}";
                    String url2 = "http://" + url +"/rpi";
                    //String url = "http://cs4720.cs.virginia.edu/rpi/?username=krj9cr";
                    HttpClient httpclient = new DefaultHttpClient();
                    HttpPost httpPost = new HttpPost(url2);
                    httpPost.setEntity(new StringEntity(json));
                    HttpResponse response2 = httpclient.execute(httpPost);
                    System.out.println("Sent request");
                    System.out.println(response2.toString());
                } catch (Exception e) {
                    System.err.println("Womp womp");
                    e.printStackTrace(System.out);
                }
            }
        }).start();
    }
    */
    public void swtichToAudioRecordTest(View v) {
        startActivity(new Intent(getApplicationContext(),RecordAudio.class));
    }



    //WOOOO RECORDING STUFF
    private static final String LOG_TAG = "RecordAudio";
    private static String mFileName = null;

    //private RecordButton mRecordButton = null;
    private MediaRecorder mRecorder = null;

    //private PlayButton mPlayButton = null;
    private MediaPlayer mPlayer = null;

    private void onRecord(boolean start, View v) {
        if (start) {
            startRecording(v);
        } else {
            stopRecording();
        }
    }

    private void onPlay(boolean start) {
        if (start) {
            startPlaying();
        } else {
            stopPlaying();
        }
    }

    private void startPlaying() {
        mPlayer = new MediaPlayer();
        try {
            mPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);

            mPlayer.setDataSource(mFileName);
            mPlayer.prepare();
            mPlayer.start();
        } catch (IOException e) {
            Log.e(LOG_TAG, "prepare() failed");
        }
    }

    private void stopPlaying() {
        mPlayer.release();
        mPlayer = null;
    }

    private void startRecording(final View v) {
        mRecorder = new MediaRecorder();
        mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        mRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        fileCount  = new File(String.valueOf(newdir)).listFiles().length;
        recordName = "NewRecording" + Integer.toString(fileCount+1);
        mFileName = newdir +"/" +recordName+".3gp";
        mRecorder.setOutputFile(mFileName);
        mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        try {
            mRecorder.prepare();
        } catch (IOException e) {
            Log.e(LOG_TAG, "prepare() failed");
        }

        startTime = SystemClock.uptimeMillis();
        customHandler.postDelayed(updateTimerThread, 0);

        //make save and delete buttons gone
        ImageButton save = (ImageButton) findViewById(R.id.save);
        save.setVisibility(View.GONE);
        ImageButton delete = (ImageButton) findViewById(R.id.delete);
        delete.setVisibility(View.GONE);


        mRecorder.start();
        //Timer timer = new Timer();
        //MyTimer mt = new MyTimer();
        //timer.schedule(mt, 1000, 3000);
    }

    /*class MyTimer extends TimerTask {

        public void run() {

            //This runs in a background thread.
            //We cannot call the UI from this thread, so we must call the main UI thread and pass a runnable
            runOnUiThread(new Runnable() {

                public void run() {
                    TextView a = (TextView) findViewById(R.id.amp);
                    final double amplitude = getAmplitude();
                    a.setText(String.valueOf(amplitude));
                    final EditText e = (EditText) findViewById(R.id.audio_ip);
                    //makeRequest(amplitude,e.getText());
                    new Thread(new Runnable() {
                        public void run() {
                            try {
                                double intensity = 0.0;//amplitude / 32767.0;
                                int red = 0;
                                int green = 0;
                                int blue = 0;
                                if (amplitude >= 30000.0) {
                                    intensity = 1.0;
                                    red = 255;
                                    green = 0;
                                    blue = 0;
                                }
                                else if (amplitude < 30000.0 && amplitude >= 20000.0) {
                                    intensity = 0.5;
                                    green = 255;
                                    blue = 255;
                                    red = 0;
                                }
                                else if (amplitude < 20000.0 && amplitude >= 10000.0) {
                                    intensity = 0.2;
                                    green = 255;
                                    blue = 0;
                                    red = 0;
                                }
                                String json = "{\"lights\": [{\"lightId\": 1, \"red\": "+String.valueOf(red)+",\"green\": "+String.valueOf(green)+",\"blue\": "+String.valueOf(blue)+", \"intensity\": " + String.valueOf(intensity) + "}],\"propagate\": true}";
                                String url2 = "http://" + e.getText() + "/rpi";
                                //String url = "http://cs4720.cs.virginia.edu/rpi/?username=krj9cr";
                                HttpClient httpclient = new DefaultHttpClient();
                                HttpPost httpPost = new HttpPost(url2);
                                httpPost.setEntity(new StringEntity(json));
                                HttpResponse response2 = httpclient.execute(httpPost);
                                System.out.println("Sent request");
                                //System.out.println(response2.toString());
                            } catch (Exception e) {
                                System.err.println("Womp womp");
                                e.printStackTrace(System.out);
                            }
                        }
                    }).start();
                }
            });
        }
    }*/


    private void stopRecording() {
        mRecorder.stop();
        mRecorder.release();
        mRecorder = null;
        timeSwapBuff += timeInMilliseconds;
        customHandler.removeCallbacks(updateTimerThread);

        ImageButton save = (ImageButton) findViewById(R.id.save);
        save.setVisibility(View.VISIBLE);
        ImageButton delete = (ImageButton) findViewById(R.id.delete);
        delete.setVisibility(View.VISIBLE);
    }

    boolean mStartRecording = true;

    public void record(View v) {

        onRecord(mStartRecording, v);
        ImageButton rec = (ImageButton) findViewById(R.id.record);
        if (mStartRecording) {
            //rec.setText("Stop Recording");
            rec.setImageResource(R.drawable.record_pause);
        } else {
            //rec.setText("Start Recording");
            rec.setImageResource(R.drawable.record_mic);
        }
        mStartRecording = !mStartRecording;
    }


    boolean mStartPlaying = true;

    public void play(View v) {
        onPlay(mStartPlaying);
        Button pla = (Button) findViewById(R.id.PlayButton);
        if (mStartPlaying) {
            pla.setText("Stop Playing");
        } else {
            pla.setText("Start Playing");
        }
        mStartPlaying = !mStartPlaying;
    }

    public Main() {
        mFileName = Environment.getExternalStorageDirectory().getAbsolutePath();
        newdir = new File(Environment.getExternalStorageDirectory(),"Record");
        if (!newdir.exists()) {
            newdir.mkdirs();
        }


        //mFileName += "/recordaudio.3gp";

        //recordName = "NewRecordingg" + Integer.toString(fileCount+1);
        //mFileName = newdir +"/" +recordName+".3gp";

    }


    @Override
    public void onPause() {
        super.onPause();
        if (mRecorder != null) {
            mRecorder.release();
            mRecorder = null;
        }

        if (mPlayer != null) {
            mPlayer.release();
            mPlayer = null;
        }
    }

    public double getAmplitude() {
        if (mRecorder != null)
            return  mRecorder.getMaxAmplitude();
        else
            return 0;

    }

    public void showMaxAmplitude(View v) {
        TextView textView = (TextView) findViewById(R.id.amp);
        textView.setText(String.valueOf(getAmplitude()));
    }

    private Runnable updateTimerThread = new Runnable() {
        public void run() {
            timeInMilliseconds = SystemClock.uptimeMillis() - startTime;
            updatedTime = timeSwapBuff + timeInMilliseconds;
            int secs = (int) (updatedTime / 1000);
            int mins = secs / 60;
            secs = secs % 60;
            int milliseconds = (int) (updatedTime % 1000);
            String m1 = Integer.toString(milliseconds);
            m1 = m1.substring(0, m1.length() - 1);
            if (m1.length() == 1) {
                m1 = "0" + m1;
            }
            else if (m1.length() < 1) {
                m1 = "00";
            }
            TextView timerValue = (TextView) findViewById(R.id.time);
            if (mins < 10) {
                timerValue.setText("0" + mins + ":"
                        + String.format("%02d", secs) + ":"
                        + m1);
                        //+ String.format("%03d", milliseconds));
            }
            else {
                timerValue.setText("" + mins + ":"
                        + String.format("%02d", secs) + ":"
                        + m1);
                        //+ String.format("%03d", milliseconds));
            }
            customHandler.postDelayed(this, 0);
        }
    };

    public void save(View v) {
        final Dialog dialog = new Dialog(context);
        dialog.setContentView(R.layout.savedialog);
        dialog.setTitle("Save as...");



        Button dialogButton = (Button) dialog.findViewById(R.id.dialogButtonOK);
        dialogButton.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dialog.dismiss();
                EditText rename = (EditText)dialog.findViewById(R.id.rename);
                String strReName = rename.getText().toString().trim();
                File to  = new File(newdir, strReName +".3gp");
                File from =  new File(mFileName );
                from.renameTo(to);


            }
        });
        dialog.show();




        recording_list.add(mFileName);
        fragmentTab1.list = recording_list;


    }
}

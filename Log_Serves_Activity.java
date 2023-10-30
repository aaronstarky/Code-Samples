package com.example.tennistrackermanual.Activities;

import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.example.tennistrackermanual.Database.DatabaseHelper;
import com.example.tennistrackermanual.Database.TennisTrackerDatabase;
import com.example.tennistrackermanual.Model.Serve;
import com.example.tennistrackermanual.Model.ServeLog;
import com.example.tennistrackermanual.R;

public class LogServesActivity extends AppCompatActivity {

    private SQLiteDatabase db;
    private TennisTrackerDatabase dbHelper;

    int totalServes;
    int servesIn;
    int kickServes;
    int kickServesIn;
    int flatServes;
    int flatServesIn;
    int sliceServes;
    int sliceServesIn;
    int customServes;
    int customServesIn;

    ServeLog serveLog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log_serves);

        // Create a new database helper
        dbHelper = new TennisTrackerDatabase(this);

        totalServes = 0;
        servesIn = 0;
        flatServes = 0;
        flatServesIn = 0;
        kickServes = 0;
        kickServesIn = 0;
        sliceServes = 0;
        sliceServesIn = 0;
        customServes = 0;
        customServesIn = 0;

        serveLog = new ServeLog();

        // Initialize stat textviews and their predetermined orders

        TextView flatLabel = new TextView(this);
        flatLabel.setText(R.string.flat_label);
        flatLabel.setTag(0);
        TextView flatStats = new TextView(this);
        flatStats.setTag(0);

        TextView kickLabel = new TextView(this);
        kickLabel.setText(R.string.kick_label);
        kickLabel.setTag(1);
        TextView kickStats = new TextView(this);
        kickStats.setTag(1);

        TextView sliceLabel = new TextView(this);
        sliceLabel.setText(R.string.slice_label);
        sliceLabel.setTag(2);
        TextView sliceStats = new TextView(this);
        sliceStats.setTag(2);

        TextView customLabel = new TextView(this);
        customLabel.setText(R.string.custom_label);
        customLabel.setTag(3);
        TextView customStats = new TextView(this);
        customStats.setTag(3);

        // Initialize buttons

        RadioGroup courtSide = findViewById(R.id.radio_group_court_side);
        Spinner serveTypeSpinner = findViewById(R.id.dropdown_serve_type);
        serveTypeSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                EditText customServe = findViewById(R.id.custom_serve_edit_text);
                if (position == parent.getCount() - 1) {
                    customServe.setVisibility(View.VISIBLE);
                    return;
                }
                customServe.setVisibility(View.INVISIBLE);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });
        TextView totalServesView = findViewById(R.id.total_serves_text_view);


        LinearLayout serveTypeLabels = findViewById(R.id.serve_type_label_list);
        LinearLayout serveNumbers = findViewById(R.id.serve_numbers_list);

        Button inButton = findViewById(R.id.green_button);
        Button outButton = findViewById(R.id.red_button);

        inButton.setEnabled(false);
        outButton.setEnabled(false);

        inButton.setOnClickListener(v -> {
            int serveTypeIndex = (int) serveTypeSpinner.getSelectedItemId();
            RadioButton clickedButton = findViewById(courtSide.getCheckedRadioButtonId());
            boolean isDeuce = !clickedButton.getText().equals("Ad");

            if (serveTypeIndex == 0) {
                if (serveLog.flatServesEmpty()) {
                    serveTypeLabels.addView(flatLabel);
                    serveNumbers.addView(flatStats);
                }
                flatServes++;
                flatServesIn++;
                serveLog.AddServe(new Serve(Serve.ServeType.FLAT, isDeuce, true));
                String newStats = flatServesIn + "/" + flatServes + " - - - " + shortenDoubleToNumDigits(calculatePercentage(flatServesIn, flatServes), 4) + "%";
                flatStats.setText(newStats);
            } else if (serveTypeIndex == 1) {
                if (serveLog.kickServesEmpty()) {
                    serveTypeLabels.addView(kickLabel);
                    serveNumbers.addView(kickStats);
                }
                kickServes++;
                kickServesIn++;
                serveLog.AddServe(new Serve(Serve.ServeType.KICK, isDeuce, true));
                String newStats = kickServesIn + "/" + kickServes + " - - - " + shortenDoubleToNumDigits(calculatePercentage(kickServesIn, kickServes), 4) + "%";
                kickStats.setText(newStats);
            } else if (serveTypeIndex == 2) {
                if (serveLog.sliceServesEmpty()) {
                    serveTypeLabels.addView(sliceLabel);
                    serveNumbers.addView(sliceStats);
                }
                sliceServes++;
                sliceServesIn++;
                serveLog.AddServe(new Serve(Serve.ServeType.SLICE, isDeuce, true));
                String newStats = sliceServesIn + "/" + sliceServes + " - - - " + shortenDoubleToNumDigits(calculatePercentage(sliceServesIn, sliceServes), 4) + "%";
                sliceStats.setText(newStats);
            } else {
                if (serveLog.customServesEmpty()) {
                    serveTypeLabels.addView(customLabel);
                    serveNumbers.addView(customStats);
                }
                customServes++;
                customServesIn++;
                serveLog.AddServe(new Serve(Serve.ServeType.CUSTOM, isDeuce, true));
                String newStats = customServesIn + "/" + customServes + " - - - " + shortenDoubleToNumDigits(calculatePercentage(customServesIn, customServes), 4) + "%";
                customStats.setText(newStats);
            }
            sortServeTypes(serveTypeLabels);
            sortServeTypes(serveNumbers);
            totalServes++;
            servesIn++;
            totalServesView.setText(generateNewTotalText());
        });
        outButton.setOnClickListener(v -> {
            int serveTypeIndex = (int) serveTypeSpinner.getSelectedItemId();
            RadioButton clickedButton = findViewById(courtSide.getCheckedRadioButtonId());
            boolean isDeuce = !clickedButton.getText().equals("Ad");

            if (serveTypeIndex == 0) {
                if (serveLog.flatServesEmpty()) {
                    serveTypeLabels.addView(flatLabel);
                    serveNumbers.addView(flatStats);
                }
                flatServes++;
                serveLog.AddServe(new Serve(Serve.ServeType.FLAT, isDeuce, false));
                String newStats = flatServesIn + "/" + flatServes + " - - - " + shortenDoubleToNumDigits(calculatePercentage(flatServesIn, flatServes), 4);
                flatStats.setText(newStats);
            } else if (serveTypeIndex == 1) {
                if (serveLog.kickServesEmpty()) {
                    serveTypeLabels.addView(kickLabel);
                    serveNumbers.addView(kickStats);
                }
                kickServes++;
                serveLog.AddServe(new Serve(Serve.ServeType.KICK, isDeuce, false));
                String newStats = kickServesIn + "/" + kickServes + " - - - " + shortenDoubleToNumDigits(calculatePercentage(kickServesIn, kickServes), 4);
                kickStats.setText(newStats);
            } else if (serveTypeIndex == 2) {
                if (serveLog.sliceServesEmpty()) {
                    serveTypeLabels.addView(sliceLabel);
                    serveNumbers.addView(sliceStats);
                }
                sliceServes++;
                serveLog.AddServe(new Serve(Serve.ServeType.SLICE, isDeuce, false));
                String newStats = sliceServesIn + "/" + sliceServes + " - - - " + shortenDoubleToNumDigits(calculatePercentage(sliceServesIn, sliceServes), 4);
                sliceStats.setText(newStats);
            } else {
                if (serveLog.customServesEmpty()) {
                    serveTypeLabels.addView(customLabel);
                    serveNumbers.addView(customStats);
                }
                customServes++;
                serveLog.AddServe(new Serve(Serve.ServeType.CUSTOM, isDeuce, false));
                String newStats = customServesIn + "/" + customServes + " - - - " + shortenDoubleToNumDigits(calculatePercentage(customServesIn, customServes), 4);
                customStats.setText(newStats);
            }
            sortServeTypes(serveTypeLabels);
            sortServeTypes(serveNumbers);
            totalServes++;
            totalServesView.setText(generateNewTotalText());
        });
        courtSide.setOnCheckedChangeListener((group, checkedId) -> {
            inButton.setEnabled(true);
            outButton.setEnabled(true);
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_log_serve, menu);
        // Get the ActionBar object
        ActionBar actionBar = getSupportActionBar();
        // Set the custom view for the ActionBar
        assert actionBar != null;
        actionBar.setTitle("New Serve Log");
        actionBar.setDisplayHomeAsUpEnabled(true);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        switch (item.getItemId()) {
            case android.R.id.home:
                builder.setTitle("Exit serve log session");
                builder.setMessage("If you leave, your changes will not be saved.\nAre you sure you want to leave?");
                // Set the positive button text and click listener
                builder.setPositiveButton("Yes", (dialog1, id) -> {
                    // User clicked OK button
                    Intent intent = new Intent(this, ServesActivity.class);
                    startActivity(intent);
                });
                builder.setNegativeButton("Cancel", (dialog1, id) -> {});
                // Create the AlertDialog object and show it
                AlertDialog dialog1 = builder.create();
                dialog1.show();
                return true;
            case R.id.action_save:
                builder.setTitle("Save");
                builder.setMessage("Are you ready to save your serve log?");
                // Set the positive button text and click listener
                builder.setPositiveButton("Yes", (dialog2, id) -> {

                    DatabaseHelper databaseHelper = new DatabaseHelper(LogServesActivity.this);

                    boolean success = databaseHelper.addServeLog(serveLog);
                    if (success) {
                        Intent intent = new Intent(this, ServesActivity.class);
                        startActivity(intent);
                        Toast.makeText(this, "Serve log saved", Toast.LENGTH_SHORT).show();
                    }
                });
                // Set the negative button text and click listener
                builder.setNegativeButton("Cancel", (dialog2, id) -> {});
                // Create the AlertDialog object and show it
                AlertDialog dialog2 = builder.create();
                dialog2.show();
                return true;
            default:
                return true;
        }
    }


    private String generateNewTotalText() {
        String servePercentage = String.valueOf(getServePercentage());
        if (servePercentage.length() > 5) {
            servePercentage = servePercentage.substring(0, 4);
        }
        return "Total: " + servesIn + "/" + totalServes +
                " - " + servePercentage + "%";
    }

    private void sortServeTypes(LinearLayout linearLayout) {
        for (int i = 0; i < linearLayout.getChildCount(); i++) {
            for (int j = i + 1; j < linearLayout.getChildCount(); j++) {
                View view1 = linearLayout.getChildAt(i);
                View view2 = linearLayout.getChildAt(j);

                int tag1 = (int) view1.getTag();
                int tag2 = (int) view2.getTag();

                if (tag1 > tag2) {
                    linearLayout.removeViewAt(j);
                    linearLayout.addView(view2, i);
                    linearLayout.removeViewAt(i + 1);
                    linearLayout.addView(view1, j);
                }
            }
        }
    }

    private static String shortenDoubleToNumDigits(double value, int numDigits) {
        String formattedValue = String.valueOf(value);
        if (formattedValue.length() > 5) {
            formattedValue = formattedValue.substring(0, 4);
        }
        return formattedValue;
    }

    private double getServePercentage() {
        return ((double) servesIn / (double) totalServes) * 100;
    }

    private double calculatePercentage(int numerator, int denominator) {
        return ((double) numerator / (double) denominator) * 100;
    }


}
import customtkinter as ctk
import subprocess
import threading
import os
import sys
from tkinter import filedialog
from PIL import Image, ImageTk  # For displaying images

# Initialize the main application window
app = ctk.CTk()
app.title("Pheno-Ranker GUI")
app.geometry("800x800")
app.resizable(True, True)  # Allow window resizing

# Create a canvas and scrollbar to make the GUI scrollable
canvas = ctk.CTkCanvas(app)
scrollbar = ctk.CTkScrollbar(app, orientation="vertical", command=canvas.yview)
scrollable_frame = ctk.CTkFrame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Load and display the logo at the top
try:
    logo_img = Image.open("img/PR-logo.png")
    # Maintain aspect ratio while resizing
    original_width, original_height = logo_img.size
    desired_width = 200  # Set your desired width here
    aspect_ratio = original_height / original_width
    desired_height = int(desired_width * aspect_ratio)
    logo_img = logo_img.resize((desired_width, desired_height), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = ctk.CTkLabel(scrollable_frame, image=logo_photo, text="")
    logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
    logo_label.grid(row=0, column=0, padx=10, pady=10)
except Exception as e:
    print(f"Error loading logo image: {e}")

# List to hold reference file entries
ref_file_entries = []

# Function to update input fields based on mode
def update_mode():
    try:
        mode = mode_var.get()
        if mode == "cohort":
            # Show Reference File fields
            ref_file_label.grid()
            ref_files_frame.grid()
            add_ref_file_button.grid()
            # Hide Target File fields
            target_file_label.grid_remove()
            target_file_entry.grid_remove()
            browse_target_button.grid_remove()
        elif mode == "patient":
            # Show both Reference and Target File fields
            ref_file_label.grid()
            ref_files_frame.grid()
            add_ref_file_button.grid()
            target_file_label.grid()
            target_file_entry.grid()
            browse_target_button.grid()
    except Exception as e:
        print(f"Error in update_mode: {e}")

# Function to toggle advanced options
def toggle_advanced_options():
    if advanced_options_var.get():
        # Show advanced options
        advanced_options_frame.grid()
    else:
        # Hide advanced options
        advanced_options_frame.grid_remove()

# Function to add a new reference file entry
def add_reference_file():
    row = len(ref_file_entries) * 2  # Calculate row position
    # Create a new entry and browse button
    new_entry = ctk.CTkEntry(ref_files_frame, width=600)
    new_entry.grid(row=row, column=0, padx=10, pady=5)
    ref_file_entries.append(new_entry)
    
    def browse_ref_file():
        filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if filename:
            new_entry.delete(0, ctk.END)
            new_entry.insert(0, filename)
            output_text.insert(ctk.END, f"Reference file updated: {filename}\n")
    
    new_browse_button = ctk.CTkButton(ref_files_frame, text="Browse", command=browse_ref_file)
    new_browse_button.grid(row=row, column=1, padx=5, pady=5)

# Function to remove a reference file entry
def remove_reference_file():
    if ref_file_entries:
        entry = ref_file_entries.pop()
        entry.grid_remove()

# Browse Button for Target File
def browse_target_file():
    try:
        filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if filename:
            target_file_entry.delete(0, ctk.END)
            target_file_entry.insert(0, filename)
            output_text.insert(ctk.END, f"Target file updated: {filename}\n")
    except Exception as e:
        output_text.insert(ctk.END, f"Error selecting target file: {e}\n")

# Enhanced File Validation Function
def validate_files():
    # Validate reference files
    valid = True
    if not ref_file_entries:
        output_text.delete("1.0", ctk.END)
        output_text.insert(ctk.END, "Error: At least one reference file must be specified.\n")
        valid = False
    else:
        for entry in ref_file_entries:
            filepath = entry.get().strip()
            if not os.path.isfile(filepath):
                output_text.delete("1.0", ctk.END)
                output_text.insert(ctk.END, f"Error: Reference file '{filepath}' does not exist or is inaccessible.\n")
                valid = False
                break

    # Validate target file in patient mode
    if mode_var.get() == "patient":
        target_file = target_file_entry.get().strip()
        if not os.path.isfile(target_file):
            output_text.delete("1.0", ctk.END)
            output_text.insert(ctk.END, "Error: Target file does not exist or is inaccessible.\n")
            valid = False

    return valid

# Function to run Pheno-Ranker
def run_pheno_ranker():
    # Validate files first
    if not validate_files():
        return

    # Get the inputs from the GUI
    mode = mode_var.get()
    reference_files = [entry.get().strip() for entry in ref_file_entries]
    target_file = target_file_entry.get().strip()
    output_file = output_file_entry.get().strip()
    include_age = include_age_var.get()
    include_hpo_ascendants = include_hpo_ascendants_var.get()
    similarity_metric = similarity_metric_option.get()
    sort_by_metric = sort_by_option.get()
    max_out = max_out_entry.get().strip()
    exclude_terms = exclude_terms_entry.get().strip()
    include_terms = include_terms_entry.get().strip()
    weights_file = weights_file_entry.get().strip()
    config_file = config_file_entry.get().strip()
    append_prefixes = append_prefixes_entry.get().strip()
    alignment_output = alignment_output_var.get()
    alignment_output_path = alignment_output_path_entry.get().strip()
    export_output = export_output_var.get()
    export_output_path = export_output_path_entry.get().strip()
    cytoscape_json = cytoscape_json_var.get()
    cytoscape_json_path = cytoscape_json_path_entry.get().strip()
    graph_stats = graph_stats_var.get()
    graph_stats_path = graph_stats_path_entry.get().strip()
    max_number_var = max_number_var_entry.get().strip()
    patients_of_interest = patients_of_interest_entry.get().strip()
    poi_out_dir = poi_out_dir_entry.get().strip()
    debug_level = debug_level_entry.get().strip()
    verbose = verbose_var.get()
    no_color = no_color_var.get()
    log_output = log_output_var.get()
    log_output_path = log_output_path_entry.get().strip()
    # Add more options as needed

    # Validate required inputs based on mode
    if not reference_files:
        output_text.delete("1.0", ctk.END)
        output_text.insert(ctk.END, "Please enter at least one reference file.")
        return

    if mode == "patient":
        if not target_file:
            output_text.delete("1.0", ctk.END)
            output_text.insert(ctk.END, "Please enter the target file for patient mode.")
            return

    # Disable the run button to prevent multiple clicks
    run_button.configure(state="disabled")
    output_text.delete("1.0", ctk.END)
    output_text.insert(ctk.END, "Running Pheno-Ranker...\n")

    # Function to execute Pheno-Ranker in a separate thread
    def pheno_ranker_thread():
        try:
            # Construct the command for Pheno-Ranker
            command = ["../pheno-ranker/bin/pheno-ranker"]

            # Add reference files
            for ref_file in reference_files:
                command.extend(["-r", ref_file])

            # Add target file if in patient mode
            if mode == "patient":
                command.extend(["-t", target_file])

            # Add optional arguments based on user input
            if output_file:
                command.extend(["-o", output_file])
            if advanced_options_var.get():
                if include_age:
                    command.append("-age")
                if include_hpo_ascendants:
                    command.append("-include-hpo-ascendants")
                if similarity_metric != "hamming":  # Default is hamming
                    command.extend(["-similarity-metric-cohort", similarity_metric])
                if sort_by_metric != "hamming":  # Default is hamming
                    command.extend(["-sort-by", sort_by_metric])
                if max_out:
                    command.extend(["-max-out", max_out])
                if exclude_terms:
                    command.extend(["-exclude-terms", exclude_terms])
                if include_terms:
                    command.extend(["-include-terms", include_terms])
                if weights_file:
                    command.extend(["-w", weights_file])
                if config_file:
                    command.extend(["-config", config_file])
                if append_prefixes:
                    command.extend(["-append-prefixes", append_prefixes])
                if alignment_output:
                    if alignment_output_path:
                        command.extend(["-a", alignment_output_path])
                    else:
                        command.append("-a")
                if export_output:
                    if export_output_path:
                        command.extend(["-e", export_output_path])
                    else:
                        command.append("-e")
                if cytoscape_json:
                    if cytoscape_json_path:
                        command.extend(["-cytoscape-json", cytoscape_json_path])
                    else:
                        command.append("-cytoscape-json")
                if graph_stats:
                    if graph_stats_path:
                        command.extend(["-graph-stats", graph_stats_path])
                    else:
                        command.append("-graph-stats")
                if max_number_var:
                    command.extend(["-max-number-var", max_number_var])
                if patients_of_interest:
                    command.extend(["-poi", patients_of_interest])
                if poi_out_dir:
                    command.extend(["-poi-out-dir", poi_out_dir])
                if debug_level:
                    command.extend(["-debug", debug_level])
                if verbose:
                    command.append("-v")
                if no_color:
                    command.append("-no-color")
                if log_output:
                    if log_output_path:
                        command.extend(["-log", log_output_path])
                    else:
                        command.append("-log")
                # Add more options as needed

            # Run the Pheno-Ranker command
            result = subprocess.run(command, capture_output=True, text=True)
            # Check for errors
            if result.returncode != 0:
                raise Exception(result.stderr)

            # In cohort mode, run the R script to generate the heatmap
            if mode == "cohort":
                # Run the R script
                rscript_command = ["Rscript", "../pheno-ranker/share/r/heatmap.R"]
                r_result = subprocess.run(rscript_command, capture_output=True, text=True)
                if r_result.returncode != 0:
                    raise Exception(f"R script error:\n{r_result.stderr}")

                # Display the heatmap image in the GUI
                display_heatmap()
            else:
                # In patient mode, display the output text
                output_text.delete("1.0", ctk.END)
                output_text.insert(ctk.END, result.stdout)
        except Exception as e:
            output_text.delete("1.0", ctk.END)
            output_text.insert(ctk.END, f"Error:\n{str(e)}")
            print(f"Error in pheno_ranker_thread: {e}")
        finally:
            # Re-enable the run button
            run_button.configure(state="normal")

    # Start the thread
    threading.Thread(target=pheno_ranker_thread).start()

# Function to display the heatmap image
def display_heatmap():
    try:
        # Ensure previous images are cleared
        global heatmap_label
        if heatmap_label is not None:
            heatmap_label.grid_remove()

        # Remove the text output widget if it exists
        output_text.grid_remove()

        output_label.configure(text="Heatmap Output:")

        # Load the heatmap image
        img = Image.open("heatmap.png")
        img = img.resize((750, 500), resample=Image.LANCZOS)  # Updated line

        photo = ImageTk.PhotoImage(img)

        # Create a label to display the image
        heatmap_label = ctk.CTkLabel(scrollable_frame, image=photo, text="")
        heatmap_label.image = photo  # Keep a reference to prevent garbage collection
        heatmap_label.grid(row=14, column=0, padx=10, pady=5)
    except FileNotFoundError:
        output_text.grid()
        output_text.delete("1.0", ctk.END)
        output_text.insert(ctk.END, "Error: Heatmap image not found. Please check the output path.\n")
    except Exception as e:
        output_text.grid()
        output_text.delete("1.0", ctk.END)
        output_text.insert(ctk.END, f"Error displaying heatmap:\n{str(e)}")
        print(f"Error in display_heatmap: {e}")

# Initialize heatmap_label
heatmap_label = None

# Define the fonts
label_font = ("Arial", 14)

# Create and place the widgets using grid

# Mode Selection
mode_var = ctk.StringVar(value="cohort")
mode_label = ctk.CTkLabel(scrollable_frame, text="Select Mode:", font=label_font)
mode_label.grid(row=1, column=0, sticky="w", padx=10, pady=(10, 0))

mode_frame = ctk.CTkFrame(scrollable_frame)
mode_frame.grid(row=2, column=0, padx=10, pady=5, sticky="w")

cohort_mode_radio = ctk.CTkRadioButton(mode_frame, text="Cohort Mode (-r)", variable=mode_var, value="cohort", command=update_mode)
cohort_mode_radio.pack(side="left", padx=5)

patient_mode_radio = ctk.CTkRadioButton(mode_frame, text="Patient Mode (-r and -t)", variable=mode_var, value="patient", command=update_mode)
patient_mode_radio.pack(side="left", padx=5)

# Reference File Entries Frame
ref_file_label = ctk.CTkLabel(scrollable_frame, text="Reference Files (-r):", font=label_font)
ref_file_label.grid(row=3, column=0, sticky="w", padx=10, pady=(10, 0))

ref_files_frame = ctk.CTkFrame(scrollable_frame)
ref_files_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Add initial reference file entry
add_reference_file()

# Add Reference File Button
add_ref_file_button = ctk.CTkButton(scrollable_frame, text="Add Reference File", command=add_reference_file)
add_ref_file_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")

# Target File Entry
target_file_label = ctk.CTkLabel(scrollable_frame, text="Target File (-t):", font=label_font)
target_file_label.grid(row=6, column=0, sticky="w", padx=10, pady=(10, 0))
target_file_entry = ctk.CTkEntry(scrollable_frame, width=600)
target_file_entry.grid(row=7, column=0, padx=10, pady=5)

# Browse Button for Target File
browse_target_button = ctk.CTkButton(scrollable_frame, text="Browse", command=browse_target_file)
browse_target_button.grid(row=7, column=1, padx=5, pady=5)

# Initially hide the Target File fields if mode is "cohort"
if mode_var.get() == "cohort":
    target_file_label.grid_remove()
    target_file_entry.grid_remove()
    browse_target_button.grid_remove()

# Output File Entry
output_file_label = ctk.CTkLabel(scrollable_frame, text="Output File (-o):", font=label_font)
output_file_label.grid(row=8, column=0, sticky="w", padx=10, pady=(10, 0))
output_file_entry = ctk.CTkEntry(scrollable_frame, width=600)
output_file_entry.grid(row=9, column=0, padx=10, pady=5)

# Advanced Options Checkbox
advanced_options_var = ctk.BooleanVar(value=False)
advanced_options_checkbox = ctk.CTkCheckBox(scrollable_frame, text="Show Advanced Options", variable=advanced_options_var, command=toggle_advanced_options)
advanced_options_checkbox.grid(row=10, column=0, sticky="w", padx=10, pady=5)

# Advanced Options Frame
advanced_options_frame = ctk.CTkFrame(scrollable_frame)
advanced_options_frame.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="w")
# Initially hide the advanced options
advanced_options_frame.grid_remove()

# Include Age Checkbox
include_age_var = ctk.BooleanVar(value=False)
include_age_checkbox = ctk.CTkCheckBox(advanced_options_frame, text="Include Age (-age)", variable=include_age_var)
include_age_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=5)

# Include HPO Ascendants Checkbox
include_hpo_ascendants_var = ctk.BooleanVar(value=False)
include_hpo_ascendants_checkbox = ctk.CTkCheckBox(advanced_options_frame, text="Include HPO Ascendants (-include-hpo-ascendants)", variable=include_hpo_ascendants_var)
include_hpo_ascendants_checkbox.grid(row=1, column=0, sticky="w", padx=10, pady=5)

# Similarity Metric Option Menu
similarity_metric_label = ctk.CTkLabel(advanced_options_frame, text="Similarity Metric (-similarity-metric-cohort):", font=label_font)
similarity_metric_label.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
similarity_metric_option = ctk.StringVar(value="hamming")
similarity_metric_menu = ctk.CTkOptionMenu(advanced_options_frame, variable=similarity_metric_option, values=["hamming", "jaccard"])
similarity_metric_menu.grid(row=3, column=0, padx=10, pady=5)

# Sort By Option Menu
sort_by_label = ctk.CTkLabel(advanced_options_frame, text="Sort By (-sort-by):", font=label_font)
sort_by_label.grid(row=4, column=0, sticky="w", padx=10, pady=(10, 0))
sort_by_option = ctk.StringVar(value="hamming")
sort_by_menu = ctk.CTkOptionMenu(advanced_options_frame, variable=sort_by_option, values=["hamming", "jaccard"])
sort_by_menu.grid(row=5, column=0, padx=10, pady=5)

# Max Out Entry
max_out_label = ctk.CTkLabel(advanced_options_frame, text="Max Number of Outputs (-max-out):", font=label_font)
max_out_label.grid(row=6, column=0, sticky="w", padx=10, pady=(10, 0))
max_out_entry = ctk.CTkEntry(advanced_options_frame, width=600)
max_out_entry.grid(row=7, column=0, padx=10, pady=5)

# Exclude Terms Entry
exclude_terms_label = ctk.CTkLabel(advanced_options_frame, text="Exclude Terms (-exclude-terms):", font=label_font)
exclude_terms_label.grid(row=8, column=0, sticky="w", padx=10, pady=(10, 0))
exclude_terms_entry = ctk.CTkEntry(advanced_options_frame, width=600)
exclude_terms_entry.grid(row=9, column=0, padx=10, pady=5)

# Include Terms Entry
include_terms_label = ctk.CTkLabel(advanced_options_frame, text="Include Terms (-include-terms):", font=label_font)
include_terms_label.grid(row=10, column=0, sticky="w", padx=10, pady=(10, 0))
include_terms_entry = ctk.CTkEntry(advanced_options_frame, width=600)
include_terms_entry.grid(row=11, column=0, padx=10, pady=5)

# Weights File Entry
weights_file_label = ctk.CTkLabel(advanced_options_frame, text="Weights File (-w):", font=label_font)
weights_file_label.grid(row=12, column=0, sticky="w", padx=10, pady=(10, 0))
weights_file_entry = ctk.CTkEntry(advanced_options_frame, width=600)
weights_file_entry.grid(row=13, column=0, padx=10, pady=5)

# Browse Button for Weights File
def browse_weights_file():
    filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if filename:
        weights_file_entry.delete(0, ctk.END)
        weights_file_entry.insert(0, filename)
browse_weights_button = ctk.CTkButton(advanced_options_frame, text="Browse", command=browse_weights_file)
browse_weights_button.grid(row=13, column=1, padx=5, pady=5)

# Config File Entry
config_file_label = ctk.CTkLabel(advanced_options_frame, text="Config File (-config):", font=label_font)
config_file_label.grid(row=14, column=0, sticky="w", padx=10, pady=(10, 0))
config_file_entry = ctk.CTkEntry(advanced_options_frame, width=600)
config_file_entry.grid(row=15, column=0, padx=10, pady=5)

# Browse Button for Config File
def browse_config_file():
    filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if filename:
        config_file_entry.delete(0, ctk.END)
        config_file_entry.insert(0, filename)
browse_config_button = ctk.CTkButton(advanced_options_frame, text="Browse", command=browse_config_file)
browse_config_button.grid(row=15, column=1, padx=5, pady=5)

# Append Prefixes Entry
append_prefixes_label = ctk.CTkLabel(advanced_options_frame, text="Append Prefixes (-append-prefixes):", font=label_font)
append_prefixes_label.grid(row=16, column=0, sticky="w", padx=10, pady=(10, 0))
append_prefixes_entry = ctk.CTkEntry(advanced_options_frame, width=600)
append_prefixes_entry.grid(row=17, column=0, padx=10, pady=5)

# Alignment Output Checkbox and Entry
alignment_output_var = ctk.BooleanVar(value=False)
alignment_output_checkbox = ctk.CTkCheckBox(advanced_options_frame, text="Write Alignment File (-a)", variable=alignment_output_var)
alignment_output_checkbox.grid(row=18, column=0, sticky="w", padx=10, pady=5)

alignment_output_path_label = ctk.CTkLabel(advanced_options_frame, text="Alignment Output Path:", font=label_font)
alignment_output_path_label.grid(row=19, column=0, sticky="w", padx=10, pady=(10, 0))
alignment_output_path_entry = ctk.CTkEntry(advanced_options_frame, width=600)
alignment_output_path_entry.grid(row=20, column=0, padx=10, pady=5)

# Export Output Checkbox and Entry
export_output_var = ctk.BooleanVar(value=False)
export_output_checkbox = ctk.CTkCheckBox(advanced_options_frame, text="Export Miscellaneous JSON Files (-e)", variable=export_output_var)
export_output_checkbox.grid(row=21, column=0, sticky="w", padx=10, pady=5)

export_output_path_label = ctk.CTkLabel(advanced_options_frame, text="Export Output Path:", font=label_font)
export_output_path_label.grid(row=22, column=0, sticky="w", padx=10, pady=(10, 0))
export_output_path_entry = ctk.CTkEntry(advanced_options_frame, width=600)
export_output_path_entry.grid(row=23, column=0, padx=10, pady=5)

# Cytoscape JSON Checkbox and Entry
cytoscape_json_var = ctk.BooleanVar(value=False)
cytoscape_json_checkbox = ctk.CTkCheckBox(advanced_options_frame, text="Generate Cytoscape JSON (-cytoscape-json)", variable=cytoscape_json_var)
cytoscape_json_checkbox.grid(row=24, column=0, sticky="w", padx=10, pady=5)

cytoscape_json_path_label = ctk.CTkLabel(advanced_options_frame, text="Cytoscape JSON Path:", font=label_font)
cytoscape_json_path_label.grid(row=25, column=0, sticky="w", padx=10, pady=(10, 0))
cytoscape_json_path_entry = ctk.CTkEntry(advanced_options_frame, width=600)
cytoscape_json_path_entry.grid(row=26, column=0, padx=10, pady=5)

# Graph Stats Checkbox and Entry
graph_stats_var = ctk.BooleanVar(value=False)
graph_stats_checkbox = ctk.CTkCheckBox(advanced_options_frame, text="Generate Graph Stats (-graph-stats)", variable=graph_stats_var)
graph_stats_checkbox.grid(row=27, column=0, sticky="w", padx=10, pady=5)

graph_stats_path_label = ctk.CTkLabel(advanced_options_frame, text="Graph Stats Path:", font=label_font)
graph_stats_path_label.grid(row=28, column=0, sticky="w", padx=10, pady=(10, 0))
graph_stats_path_entry = ctk.CTkEntry(advanced_options_frame, width=600)
graph_stats_path_entry.grid(row=29, column=0, padx=10, pady=5)

# Max Number Var Entry
max_number_var_label = ctk.CTkLabel(advanced_options_frame, text="Max Number of Variables (-max-number-var):", font=label_font)
max_number_var_label.grid(row=30, column=0, sticky="w", padx=10, pady=(10, 0))
max_number_var_entry = ctk.CTkEntry(advanced_options_frame, width=600)
max_number_var_entry.grid(row=31, column=0, padx=10, pady=5)

# Patients of Interest Entry
patients_of_interest_label = ctk.CTkLabel(advanced_options_frame, text="Patients of Interest (-poi):", font=label_font)
patients_of_interest_label.grid(row=32, column=0, sticky="w", padx=10, pady=(10, 0))
patients_of_interest_entry = ctk.CTkEntry(advanced_options_frame, width=600)
patients_of_interest_entry.grid(row=33, column=0, padx=10, pady=5)

# POI Output Directory Entry
poi_out_dir_label = ctk.CTkLabel(advanced_options_frame, text="POI Output Directory (-poi-out-dir):", font=label_font)
poi_out_dir_label.grid(row=34, column=0, sticky="w", padx=10, pady=(10, 0))
poi_out_dir_entry = ctk.CTkEntry(advanced_options_frame, width=600)
poi_out_dir_entry.grid(row=35, column=0, padx=10, pady=5)

# Debug Level Entry
debug_level_label = ctk.CTkLabel(advanced_options_frame, text="Debug Level (-debug):", font=label_font)
debug_level_label.grid(row=36, column=0, sticky="w", padx=10, pady=(10, 0))
debug_level_entry = ctk.CTkEntry(advanced_options_frame, width=600)
debug_level_entry.grid(row=37, column=0, padx=10, pady=5)

# Verbose Checkbox
verbose_var = ctk.BooleanVar(value=False)
verbose_checkbox = ctk.CTkCheckBox(advanced_options_frame, text="Verbose Output (-v)", variable=verbose_var)
verbose_checkbox.grid(row=38, column=0, sticky="w", padx=10, pady=5)

# No Color Checkbox
no_color_var = ctk.BooleanVar(value=False)
no_color_checkbox = ctk.CTkCheckBox(advanced_options_frame, text="No Color Output (-no-color)", variable=no_color_var)
no_color_checkbox.grid(row=39, column=0, sticky="w", padx=10, pady=5)

# Log Output Checkbox and Entry
log_output_var = ctk.BooleanVar(value=False)
log_output_checkbox = ctk.CTkCheckBox(advanced_options_frame, text="Save Log File (-log)", variable=log_output_var)
log_output_checkbox.grid(row=40, column=0, sticky="w", padx=10, pady=5)

log_output_path_label = ctk.CTkLabel(advanced_options_frame, text="Log Output Path:", font=label_font)
log_output_path_label.grid(row=41, column=0, sticky="w", padx=10, pady=(10, 0))
log_output_path_entry = ctk.CTkEntry(advanced_options_frame, width=600)
log_output_path_entry.grid(row=42, column=0, padx=10, pady=5)

# Run Button
run_button = ctk.CTkButton(scrollable_frame, text="Run Pheno-Ranker", command=run_pheno_ranker)
run_button.grid(row=12, column=0, padx=10, pady=15)

# Output Label
output_label = ctk.CTkLabel(scrollable_frame, text="Pheno-Ranker Output:", font=label_font)
output_label.grid(row=13, column=0, sticky="w", padx=10, pady=(20, 5))

# Output Text Box
output_text = ctk.CTkTextbox(scrollable_frame, height=250, width=750)
output_text.grid(row=14, column=0, padx=10, pady=5)

# Place the canvas and scrollbar in the main window
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Set initial mode
update_mode()

# Start the application's event loop
if __name__ == '__main__':
    app.mainloop()

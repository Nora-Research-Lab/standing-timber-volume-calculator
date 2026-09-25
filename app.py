import gradio as gr
import pandas as pd
import tempfile
import os
from standing_timber_volume_calculator import (
    SPECIES_DEFAULTS,
    get_form_factor,
    calculate_individual_volume,
    calculate_stand_volume,
    convert_to_board_feet,
    classify_volume,
    get_species_average_volume,
    generate_comparison_plot
)

def calculate_and_display(species, dbh, height, trees_per_ha, use_custom_ff, custom_ff):
    # Validate inputs
    if dbh is None or dbh <= 0:
        return "DBH must be positive.", None, None, None
    if height is None or height <= 0:
        return "Height must be positive.", None, None, None
    if trees_per_ha is None or trees_per_ha <= 0:
        trees_per_ha = 1
    try:
        ff = get_form_factor(species, custom_ff if use_custom_ff else None)
    except ValueError as e:
        return str(e), None, None, None

    vol_m3 = calculate_individual_volume(dbh, height, ff)
    stand_m3 = calculate_stand_volume(vol_m3, trees_per_ha)
    vol_bft = convert_to_board_feet(vol_m3)
    stand_bft = convert_to_board_feet(stand_m3)
    classification = classify_volume(vol_m3)
    species_avg = get_species_average_volume(species)

    # Build output text
    output_text = (
        f"**Individual Tree Volume:** {vol_m3:.3f} m³ ({vol_bft:.0f} board feet)\n"
        f"**Stand Volume per ha:** {stand_m3:.3f} m³/ha ({stand_bft:.0f} board feet/ha)\n"
        f"**Size Classification:** {classification}\n"
        f"**Form factor used:** {ff:.3f}\n"
        f"**Species average volume (reference):** {species_avg:.3f} m³"
    )

    # Generate plot
    plot = generate_comparison_plot(vol_m3, species)

    # Prepare CSV content for download
    csv_data = {
        "Species": [species],
        "DBH (cm)": [dbh],
        "Height (m)": [height],
        "Form Factor": [ff],
        "Trees per ha": [trees_per_ha],
        "Individual Volume (m3)": [vol_m3],
        "Individual Volume (bft)": [vol_bft],
        "Stand Volume (m3/ha)": [stand_m3],
        "Stand Volume (bft/ha)": [stand_bft],
        "Classification": [classification]
    }
    df = pd.DataFrame(csv_data)
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w")
    df.to_csv(temp_path.name, index=False)
    temp_path.close()

    return output_text, plot, temp_path.name, temp_path.name  # file path for download

# Build Gradio UI
with gr.Blocks(title="Standing Timber Volume Calculator") as demo:
    gr.Markdown("## Standing Timber Volume Calculator")
    gr.Markdown("Estimate merchantable timber volume for a single tree or uniform stand.")

    with gr.Row():
        species_dd = gr.Dropdown(
            choices=list(SPECIES_DEFAULTS.keys()),
            value="Douglas-fir",
            label="Tree Species"
        )
        dbh_input = gr.Number(
            minimum=5.0, maximum=200.0, value=30.0, step=0.1,
            label="Diameter at Breast Height (cm)"
        )
        height_input = gr.Number(
            minimum=1.0, maximum=60.0, value=20.0, step=0.1,
            label="Tree Height (m)"
        )
        trees_input = gr.Number(
            minimum=1, maximum=10000, value=1, step=1,
            label="Trees per hectare (stems/ha)"
        )

    with gr.Row():
        use_custom_ff = gr.Checkbox(label="Use custom form factor")
        custom_ff_input = gr.Number(
            minimum=0.3, maximum=0.7, value=0.45, step=0.01,
            label="Custom Form Factor",
            visible=False
        )

    # Show/hide custom form factor based on checkbox
    def toggle_custom_ff(checked):
        return gr.update(visible=checked)
    use_custom_ff.change(toggle_custom_ff, inputs=use_custom_ff, outputs=custom_ff_input)

    calc_btn = gr.Button("Calculate Volume")

    # Outputs
    output_text = gr.Markdown()
    output_plot = gr.Plot(label="Volume Comparison")
    download_btn = gr.DownloadButton(label="Download Results as CSV", interactive=False)
    csv_state = gr.State(value=None)

    calc_btn.click(
        fn=calculate_and_display,
        inputs=[species_dd, dbh_input, height_input, trees_input, use_custom_ff, custom_ff_input],
        outputs=[output_text, output_plot, download_btn, csv_state]
    )

    # Enable download after calculation
    def enable_download(file_path):
        return gr.update(value=file_path, interactive=True) if file_path else gr.update(interactive=False)
    csv_state.change(enable_download, inputs=csv_state, outputs=download_btn)

demo.launch(server_name="0.0.0.0", server_port=7860)

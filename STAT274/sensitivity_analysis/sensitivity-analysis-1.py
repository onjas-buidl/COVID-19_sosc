from austen_plots.AustenPlot import AustenPlot
import os

input_df_path = './example_data/input_df.csv'
bias = 2.0

# if you have no covariate controls skip specifying covariate_dir_path
# covariate_dir_path = None
covariate_dir_path = './example_data/covariates/'

ap = AustenPlot(input_df_path, covariate_dir_path)
p, plot_coords, variable_coords = ap.fit(bias=2.0)
# or if you would like to calculate an Austen plot using ATT instead
p, plot_coords, variable_coords = ap.fit(bias=2.0, do_att=True)

#save outputs
output_dir = './example_data/output/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

p.save(os.path.join(output_dir,
                        'austen_plot.png'), dpi=500, verbose=False)
plot_coords.to_csv(os.path.join(output_dir, 'plot_coords.csv'), index=False)
variable_coords.to_csv(os.path.join(output_dir, 'variable_coords.csv'), index=False)
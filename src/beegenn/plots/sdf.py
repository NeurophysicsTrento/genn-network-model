import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from .data_manager import DataManager


def plot_sdf_heatmap_per_pop(sdf_average, t_start, t_end, dt, pop, subplot):
    res = subplot.imshow(sdf_average, vmin = 0, vmax = 100, cmap = 'plasma')
    subplot.set_aspect((t_end-t_start)//10)
    subplot.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([3000*i//dt for i in range(int(t_end-t_start)//3000 + 1)]))
    subplot.set_xticklabels([f"{t_start * (i + 1):.1g}" for i in range(int(t_end-t_start)//3000 + 1)], rotation=45, fontsize = 8)
    subplot.set_title(pop)
    subplot.set_xlabel("Time [ms]")
    subplot.set_ylabel("Glomeruli")
    return res

def plot_sdf_over_time_outliers(sdf_matrix_avg, subplot):
    glomeruli_mean_sdf = np.mean(sdf_matrix_avg, axis = 1)
    global_mean = np.mean(glomeruli_mean_sdf)
    global_sdt = np.std(glomeruli_mean_sdf)
    glomeruli_of_interest = []

    for (i, mean_sdf) in enumerate(glomeruli_mean_sdf):
        if np.abs(mean_sdf - global_mean) > global_sdt:
            glomeruli_of_interest.append(i)

    for i in glomeruli_of_interest:
        subplot.plot(sdf_matrix_avg[i, :], label = f"Glomerulus {i}")
    subplot.legend()

def get_subplots(n_pops):
    figure, subplots = plt.subplots(
        1, n_pops, sharey=True, layout="constrained")
    return figure, subplots

def colorbar(image, subplot, figure):
    cbar = figure.colorbar(image, ax=subplot)
    cbar.ax.set_ylabel("SDF ($Hz$)")

def plot_sdf_heatmap(pops, t_start, t_end, data_manager, show):

    figure, subplots = get_subplots(len(pops))
    image = []

    for (pop, subplot) in zip(pops, subplots):
        sdf_avg = data_manager.sdf_per_glomerulus_avg(
                pop,
                t_start,
                t_end
                )
        image.append(
                plot_sdf_heatmap_per_pop(
                    sdf_avg,
                    t_start,
                    t_end,
                    data_manager.get_sim_dt(),
                    pop,
                    subplot
                    )
                )
    colorbar(image[-1], subplots[-1], figure)
    filename = f"sdf/{t_start:.1f}_{t_end:.1f}.png"
    data_manager.show_or_save(filename, show)

if __name__ == "__main__":
    from beegenn.parameters.reading_parameters import parse_cli
    from pathlib import Path
    import pandas as pd
    param = parse_cli()
    data_manager = DataManager(param['simulations']['simulation'], param['simulations']
                 ['name'], param['neuron_populations'], param['synapses'])

    events = pd.read_csv(Path(param['simulations']['simulation']['output_path']) / param['simulations']['name'] / 'events.csv')

    plot_sdf_heatmap(['orn', 'pn', 'ln'], 9000, 12000, data_manager, show = False)

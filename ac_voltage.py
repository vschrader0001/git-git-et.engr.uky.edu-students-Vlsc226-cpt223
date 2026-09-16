import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from math import pi
    from sciform import SciNum
    import pygit2

    return mo, np, pi, plt, pygit2


@app.cell(hide_code=True)
def _(
    amplitude_default,
    amplitude_end,
    amplitude_start,
    amplitude_step,
    frequency_default,
    frequency_end,
    frequency_start,
    frequency_step,
    get_amplitude,
    get_frequency,
    mo,
    phase_default,
    phase_end,
    phase_start,
    phase_step,
    set_amplitude,
    set_frequency,
    set_phase,
):
    # UI elements

    frequency = mo.ui.slider(
        start=frequency_start,
        stop=frequency_end,
        step=frequency_step,
        value=get_frequency(),
        on_change=set_frequency,
        label="Frequency",
    )
    amplitude = mo.ui.slider(
        start=amplitude_start,
        stop=amplitude_end,
        step=amplitude_step,
        value=get_amplitude(),
        on_change=set_amplitude,
        label="Amplitude",
    )
    phase = mo.ui.slider(
        start=phase_start,
        stop=phase_end,
        step=phase_step,
        value=get_amplitude(),
        on_change=set_phase,
        label="Phase",
    )

    def ui_reset(value):
        set_frequency(frequency_default)
        set_amplitude(amplitude_default)
        set_phase(phase_default)

    reset = mo.ui.button(label="Reset", on_click=ui_reset)

    # Repo refresh button and state
    refresh_button = mo.ui.refresh(
        options=["1m", "10m"],
        default_interval="10m",
    )
    return amplitude, frequency, phase, refresh_button, reset


@app.cell(hide_code=True)
def _(mo):
    # UI state

    frequency_start = 1.0 # Hz
    frequency_end = 10.0 # Hz
    frequency_step = 0.1 # Hz
    frequency_default = frequency_start

    amplitude_start = 0.1 # V
    amplitude_end = 1.0 # V
    amplitude_step = 0.05 # V
    amplitude_default = amplitude_end/2.0

    phase_start = -90 # degreee
    phase_end = 90 # degree
    phase_step = 1 # degree
    phase_default = 0

    # plot parameters
    plot_period = 1.0/frequency_start # x-axis, s
    plot_amplitude = amplitude_end    # y-axis, V

    # slider states
    get_frequency, set_frequency = mo.state(frequency_default,
                                            allow_self_loops=True)
    get_amplitude, set_amplitude = mo.state(amplitude_default,
                                            allow_self_loops=True)
    get_phase, set_phase = mo.state(phase_default,
                                    allow_self_loops=True)
    return (
        amplitude_default,
        amplitude_end,
        amplitude_start,
        amplitude_step,
        frequency_default,
        frequency_end,
        frequency_start,
        frequency_step,
        get_amplitude,
        get_frequency,
        get_phase,
        phase_default,
        phase_end,
        phase_start,
        phase_step,
        plot_amplitude,
        plot_period,
        set_amplitude,
        set_frequency,
        set_phase,
    )


@app.cell(hide_code=True)
def _(pygit2, refresh_button):
    # repo state

    repo = pygit2.Repository(".")
    last_refresh = refresh_button.value
    repo_workdir = repo.workdir
    current_branch = repo.head.shorthand
    current_commit = repo.head.target
    repo_is_clean = len(repo.status()) == 0
    return (
        current_branch,
        current_commit,
        last_refresh,
        repo_is_clean,
        repo_workdir,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Measuring AC Voltage
    """)
    return


@app.cell(hide_code=True)
def _(
    current_branch,
    current_commit,
    last_refresh,
    mo,
    repo_is_clean,
    repo_workdir,
):
    mo.md(rf"""
    ## Version Information

    **Repository:** ``{repo_workdir}``<br>
    **Current Branch:** ``{current_branch}``<br>
    **Current Commit:** ``{current_commit}``<br>
    **Clean:** ``{repo_is_clean}``<br>
    **Last Refresh:** ``{last_refresh or None}``
    """)
    return


@app.cell(hide_code=True)
def _(refresh_button):
    refresh_button
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a demonstration notebook.
    We will use it
    to demonstrate the measurement of the amplitude and frequency of a sinusoidal signal $y(t)$,
    where

    \[
    y(t) = A\sin(2\pi ft + \varphi)\,.
    \]

    ## Independent Variables

    $A$ is the amplitude, $f$ is the frequency, and $\varphi$ is the phase.
    Let us assume that the signal is represented by a voltage
    and that therefore the amplitude has a unit of Volt.

    ## Dependent Variabes

    Other useful variables are

    - Period $T=1/f$
    - Angular Frequency $\omega = 2\pi f$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interactive Plot

    The impact of amplitude, frequency, and phase can be seen in the following interactive plot:
    """)
    return


@app.cell(hide_code=True)
def _(
    amplitude,
    frequency,
    get_amplitude,
    get_frequency,
    get_phase,
    mo,
    np,
    phase,
    pi,
    plot_amplitude,
    plot_period,
    plt,
    reset,
):
    # Variables are retrieved from Marimo state objects
    # controlled by the sliders in the interactive plot

    # Frequency
    f = get_frequency()  # Hz

    # Peak Voltage
    v_p = get_amplitude()  # V

    # Phase
    phi = get_phase()*pi/180.0 # rad

    omega = 2 * pi * f

    t = np.linspace(0.0, 2.0 * plot_period, 1000)
    fig, ax = plt.subplots()
    ax.autoscale(False)
    ax.set(xlim=(t[0], t[-1]), ylim=(-plot_amplitude, +plot_amplitude))
    ax.grid(True)
    ax.plot(t, v_p * np.sin(omega * t + phi))
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Sinusoidal Voltage Signal")

    mo.vstack(
        [
            fig,
            mo.hstack([frequency, f"Frequency: {get_frequency():2.1f} Hz"]),
            mo.hstack([amplitude, f"Amplitude: {get_amplitude():-3.2f} V"]),
            mo.hstack([phase, f"Phase: {get_phase():+3.0f}º"]),
            reset,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Measurement

    Use your signal generator to generate an AC signal with a peak voltage of 5 V and a frequency of 1 kHz.
    Measure the voltage with your oscilloscope. Adjust the time base
    so that a single period of the signal is displayed.
    For easier analysis, in particular ensure that there is only a single maximum and minimum in the plot.
    Then, save the signal to a CSV file named `sine.csv`.

    ## Plotting

    Load the file via [`np.loadtxt()`](https://numpy.org/doc/2.3/reference/generated/numpy.loadtxt.html).
    Ensure that you skip the first 8 rows and the first column.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # loading code goes here

    mo.show_code()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plot the signal using `matplotlib`. Make the plot interactive.
    """)
    return


@app.cell
def _():
    # plotting code goes here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analysis

    Compute the period of the signal by finding the minimum and the maximum voltage value and their coresponding times. Then calculate the frequency.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # analysis code goes here

    mo.show_code()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Results

    Display the results in this cell, using interpolated f-strings. Display the period in milliseconds, the frequency in kilohertz, and the amplitude in volts.

    Use the [`SciNum` class](https://sciform.readthedocs.io/en/stable/usage.html#scinum)
    from the [`sciform` package](https://sciform.readthedocs.io/en/stable/)
    to format the ouput in engineering notation to 3 significant figures.
    """)
    return


if __name__ == "__main__":
    app.run()

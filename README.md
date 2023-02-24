<a name="readme-top"></a>
<!-- ========= PROJECT SHIELDS ============================================= -->

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- ========= PROJECT LOGO ================================================ -->

<br />
<p align="center">

  <h3 align="center">Taranis</h3>

  <p align="center">
    Convert MIDI to PWM wav for use with a tesla coil.
    ·
    <a href="https://github.com/SpinStabilized/taranis/issues">Report Bug</a>
    ·
    <a href="https://github.com/SpinStabilized/taranis/issues">Request Feature</a>
  </p>
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= TABLE OF CONTENTS =========================================== -->

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#references">References</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= ABOUT THE PROJECT =========================================== -->

## About The Project

<!--
[![DBot Screenshot][product-screenshot]](https://github.com/SpinStabilized/dbot)
-->

A bit of software to convert a simple MIDI file into a PWM audio wav file for
use with a musical tesla coil. Just getting started.

### Built With

* [Mido](https://mido.readthedocs.io/en/latest/index.html)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= GETTING STARTED ============================================= -->

## Getting Started

To get up and running with Taranis:

### Prerequisites

The only pre-requisites to get up and running are Python 3 with `pipenv`. While `pipenv` is not required it makes installation of packages for the project trivial.

* Python 3
  This is highly system dependent. On Windows I recommend using [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) or [Chocolatey](https://chocolatey.org/) and on OS X I can *highly* recommend [Homebrew](https://brew.sh/).
* `pipenv`
  ```sh
  pip install --user pipenv
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/SpinStabilized/taranis.git
   ```
2. The development environment uses [`pipenv`](https://pipenv.pypa.io/en/latest/#install-pipenv-today). To install a test environment
   ```sh
   pipenv install
   ```
3. To execute the bot in the `pipenv` environment you can execute it directly
   ```sh
   pipenv run src/taranis.py
   ```
   or jump into a shell in the `pipenv` environment and run it with Python
   ```sh
   pipenv shell
   python src/taranis.py
   ```
4. I develop in [VS Code](https://code.visualstudio.com/) and mostly on a macOS machine. Some of the extensions I find very useful (and should be largly cross-compatible) are
  * [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  * [Git History](https://marketplace.visualstudio.com/items?itemName=donjayamanne.githistory)
  
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= USAGE EXAMPLES ============================================== -->

## Usage

*TBD*

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= ROADMAP ===================================================== -->

## Roadmap

See the [open issues](https://github.com/SpinStabilized/taranis/issues) for a list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= CONTRIBUTING ================================================ -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= REFERENCES ================================================== -->

## References

### Converting Midi Ticks to Seconds

> The formula is 60000 / (BPM * PPQ) (milliseconds).
> 
> Where BPM is the tempo of the track (Beats Per Minute).
> 
> (i.e. a 120 BPM track would have a MIDI time of (60000 / (120 * 192)) or
> 2.604 ms for 1 tick.
> 
> If you don't know the BPM then you'll have to determine that first. MIDI
> times are entirely dependent on the track tempo.

```math
ms = \frac{60000}{BPM \times PPQ}
```

Aaronaught. “Converting MIDI Ticks to Actual Playback Seconds - Response.” Stack Overflow, January 10, 2010. https://stackoverflow.com/a/2038364. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= LICENSE ===================================================== -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= CONTACT ===================================================== -->

## Contact

Brian McLaughlin - [@bjmclaughlin](https://twitter.com/bjmclaughlin) - bjmclauglin@gmail.com

Project Link: [https://github.com/SpinStabilized/taranis](https://github.com/SpinStabilized/taranis)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= ACKNOWLEDGEMENTS ============================================ -->

## Acknowledgements
* [Mido](https://mido.readthedocs.io/en/latest/index.html)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ========= MARKDOWN LINKS & IMAGES ===================================== -->

[contributors-url]: https://github.com/SpinStabilized/taranis/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SpinStabilized/taranis?style=for-the-badge
[forks-url]: https://github.com/SpinStabilized/taranis/network/members
[stars-shield]: https://img.shields.io/github/stars/SpinStabilized/taranis?style=for-the-badge
[stars-url]:https://github.com/SpinStabilized/taranis/stargazers
[issues-shield]:https://img.shields.io/github/issues/SpinStabilized/taranis?style=for-the-badge
[issues-url]: https://github.com/SpinStabilized/taranis/issues
[license-shield]: https://img.shields.io/github/license/SpinStabilized/taranis?style=for-the-badge
[license-url]: https://github.com/SpinStabilized/taranis/blob/main/LICENSE

[so-ticks-to-secs]: https://stackoverflow.com/a/2038364

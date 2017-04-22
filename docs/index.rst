Rickshaw
===============

.. raw:: html

    <p style="text-align:center;">
    <span style="font-family:Times;font-size:28px;font-style:normal;font-weight:normal;text-decoration:none;text-transform:none;font-variant:small-caps;color:000000;">
    ~ A Stochastic Driver for Cyclus ~
    <br />
    <br />
    </span>
    </p>

Rickshaw is a Python-powered stochastic driver for Cyclus. Rickshaw will create randomly-generated,
fully-valid Cyclus input files. Rickshaw works by,

* Selecting a random fuel cycle structure by picking niches,
* Selecting random archetypes to represent those niches,
* Configure the archetypes by randomly selecting values for each state variable.

Rickshaw can run on the command line to generate JSON input files or operate in a server mode
that also runs Cyclus on the generated files. Rickshaw can interface with a variety of scheduluers,
including Docker (for a node) and Docker Swarm (for the full cluster).

=========
Contents
=========

.. toctree::
    :titlesonly:
    :maxdepth: 1

    api/index
    gettingstarted

.. .. include:: dependencies.rst


============
Contributing
============
We highly encourage contributions to rickshaw!  If you would like to contribute,
it is as easy as forking the repository on GitHub, making your changes, and
issuing a pull request.

==========
Contact Us
==========
If you have questions or comments, please contact the authors directly or
open an issue on GitHub.

=============
Helpful Links
=============

* `Documentation <http://xon.sh>`_
* `GitHub Repository <https://github.com/ergs/rickshaw>`_
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. raw:: html

    <a href="https://github.com/ergs/rickshaw" class='github-fork-ribbon' title='Fork me on GitHub'>Fork me on GitHub</a>

    <style>
    /*!
     * Adapted from
     * "Fork me on GitHub" CSS ribbon v0.2.0 | MIT License
     * https://github.com/simonwhitaker/github-fork-ribbon-css
     */

    .github-fork-ribbon, .github-fork-ribbon:hover, .github-fork-ribbon:hover:active {
      background:none;
      left: inherit;
      width: 12.1em;
      height: 12.1em;
      position: absolute;
      overflow: hidden;
      top: 0;
      right: 0;
      z-index: 9999;
      pointer-events: none;
      text-decoration: none;
      text-indent: -999999px;
    }

    .github-fork-ribbon:before, .github-fork-ribbon:after {
      /* The right and left classes determine the side we attach our banner to */
      position: absolute;
      display: block;
      width: 15.38em;
      height: 1.54em;
      top: 3.23em;
      right: -3.23em;
      box-sizing: content-box;
      transform: rotate(45deg);
    }

    .github-fork-ribbon:before {
      content: "";
      padding: .38em 0;
      background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.1));
      box-shadow: 0 0.07em 0.4em 0 rgba(0, 0, 0, 0.3);
      pointer-events: auto;
    }

    .github-fork-ribbon:after {
      content: attr(title);
      color: #000;
      font: 700 1em "Helvetica Neue", Helvetica, Arial, sans-serif;
      line-height: 1.54em;
      text-decoration: none;
      text-align: center;
      text-indent: 0;
      padding: .15em 0;
      margin: .15em 0;
      border-width: .08em 0;
      border-style: dotted;
      border-color: #777;
    }

    </style>

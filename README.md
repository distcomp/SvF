# SvF
Implementation of SvF-technology of regularized identification of mathematical models by experimental data.

The technology of balanced identification of mathematical models (the so-called SvF-technology, from Simplicity vs Fitting) proposes a promising area of applied mathematics, combining methods of structural mathematical modeling, optimization, adaptive regularization and distributed computing.

The author of the SvF-technology is [Alexander Sokolov](https://scholar.google.ru/citations?user=mtE_u_YAAAAJ&hl=en&oi=sra), [sashasok](https://gitlab.com/sashasok).

The technology and underlying mathematical algorithms are described in the following articles:
1. Sokolov A. V., Voloshinov V. V. Model Selection by Balanced Identification: the Interplay of Optimization and Distributed Computing // Open Computer Science, 2020, 10 — p. 283–295. [DOI: 10.1515/comp-2020-0116](https://doi.org/10.1515/comp-2020-0116)
2. Соколов, А.В.; Волошинов, В.В. Выбор математической модели: баланс между сложностью и близостью к измерениям. International Journal of Open Information
Technologies, 2018, 6(9) C. 33-41, [PDF](http://injoit.org/index.php/j1/article/view/612) 

Current repository is the public version of [private SvF](https://gitlab.com/sashasok/svf)

# How to cite
Please, cite the first of the above articles if you'll use the technology.

# How to clone
Current implementation of the SvF-technolosy is based on [Everest Python API](https://gitlab.com/everest/python-api) and [SSOP Everest Application](https://optmod.distcomp.org/apps/vladimirv/solve-set-opt-probs), which have to be cloned from their Git-repos. **So, use the following command for correct cloning**

`$ git clone --recurse-submodules https://github.com/distcomp/SvF.git`

or, if you have public key attached to your GITHUB account, then you can use another command:

`$ git clone --recurse-submodules git@github.com:distcomp/SvF.git`

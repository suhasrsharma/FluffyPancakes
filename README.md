# Fluffy Pancakes

Fluffy Pancakes is a library designed to detect phishing websites. It uses Machine Learning to predict the output with an accuracy of 95.2%. 

*Note: Please bear with us for a few seconds to get the output since the library is computationally intensive. We felt bad for making you wait, so we have included a progress bar that you can enable to see the percentage of progress and also the time taken for execution. Also note that the library heavily depends on a stable internet connection to function its best and to obtain the results. So, the quicker your internet connection is, the faster your results will be :).*

**You can find the PyPI package [here](https://pypi.org/project/fluffypancakes/)**

# Usage

- #### Import 
    ```py
     $ import fluffypancakes
     ```

- #### Call the function and Pass the URL 
    ```py
     $ print(fluffypancakes.serve('<website URL>', progressBar=True))
     ```

- #### Defaults
     The default value of the progressBar is 'True'. However, the option can be enabled or disabled with *boolean* 'True' or 'False' respectively.


# Output
> -1 : Legitimate Website

> 1 : Phishing Website

> "The URL entered is either Invalid or the Host is unserviceable" : For invalid URLs and Unservicable Hosts

> Sample output:
>
> ![Progress Bar](https://github.com/suhasrsharma/FluffyPancakes/blob/master/images/progressBar_inProgress.PNG)
>
> ![Progress Bar Completed](https://github.com/suhasrsharma/FluffyPancakes/blob/master/images/progressBar_complete.PNG)


The output is predicted with an accuracy of 95.2%. It is not a definitive classification. 

# Dependencies

The list of dependencies is enumerated in "requirements.txt"

You can install all the dependencies by executing the following command:

```sh
$ pip install -r requirements.txt
```

Additional dependencies:

- Chrome Driver : You'll need a chromedriver in order to complete execution of the code. You can get the file from [here](https://chromedriver.chromium.org/). Unzip and add the "chromedriver.exe" (Windows) or "chromedriver" (Linux and MacOS) file to the PYTHONPATH environment variable.

    Well, that's a lot of work right? We know! So, we have included the current stable version of the chromedriver in the [dependencies](https://github.com/suhasrsharma/FluffyPancakes/tree/master/dependencies) folder of the repo.

    The code automatically detects the OS (Windows, Linux Based and MacOS) and picks up the respective chromedriver file.

    **You're all set to go.** Although, if, by any chance, you face an issue, just add to PYTHONPATH, the directory structure to where you downloaded this repository.


# Development

Want to contribute? Great!

FluffyPancakes uses http requests, bs4, selenium, and of course, Machine Learning, and a lot more libraries. 

You can find the **PyPI** repository [here](https://pypi.org/project/fluffypancakes/).

Make sure you use the following command to get the exact versions of pytest and twine:

```sh
$ pip install -e .[dev]
```

You can find the sample test case [here](https://github.com/suhasrsharma/FluffyPancakes/blob/master/src/sample_test.py).


# Development Status
##### Development Status :: 4 - Beta
##### Version - 0.1.2
##### Operating System :: OS Independent


# License
### MIT
##### Free software? Of Course!

---

In collaboration with the [Center for ISFCR](https://www.isfcr.pes.edu/) at [PES University](https://www.pes.edu/), Bangalore, India, under the guidance of [Mr. Prasad B Honnavali](https://faculty.pes.edu/p10020).

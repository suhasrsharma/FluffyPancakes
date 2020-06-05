# Fluffy Pancakes
Fluffy Pancakes is a library designed to detect phishing websites. It uses Machine Learning to predict the output with an accuracy of 95.2%. 

*Note: Please bear with us for a few seconds to get the output since the library is computationally intensive. We felt bad for making you wait, so we have included a progress bar that you can enable to see the percentage of progress and also the time taken for execution. Also note that the library heavily depends on a stable internet connection to function its best and to obtain the results. So, the quicker your internet connection is, the faster your results will be :).*


# Usage

- #### Import 
    ```sh
     $ from fluffypancakes import FluffyPancakes
     ```

- #### Instantialize
    ```sh
     $ dessert = FluffyPancakes()
     ```

- #### Call the function and Pass the URL 
    ```sh
     $ print(dessert.serve('<website URL>', progressBar=True))
     ```

- #### Defaults
     The default value of the progressBar is 'True'. However, the option can be enabled or disabled with *boolean* 'True' or 'False' respectively.

- #### Driver
     You'll need a chromedriver in order to complete execution of the code. You can get the file from [here](https://chromedriver.chromium.org/). Unzip and add the "chromedriver.exe" (Windows) or "chromedriver" (Linux) file to the PYTHONPATH environment variable.

     Well, that's a lot of work right? We know! So, we have included the current stable version of the chromedriver in the [dependencies](https://github.com/suhasrsharma/FluffyPancakes/tree/master/dependencies) folder of the repo.

     __You're all set to go.__ Although, if, by any chance, you face an issue, just add to PYTHONPATH, the directory structure to where you downloaded this repository.


# Output
> -1 : Legitimate Website

> 1 : Phishing Website

> Sample output:
>
> ![Progress Bar](https://github.com/suhasrsharma/FluffyPancakes/blob/master/images/progressBar_inProgress.PNG)
>
> ![Progress Bar Completed](https://github.com/suhasrsharma/FluffyPancakes/blob/master/images/progressBar_complete.PNG)


The output is predicted with an accuracy of 95.2%. It is not a definitive classification. 

# Dependencies

- Chrome Driver : You'll need a chromedriver in order to complete execution of the code. You can get the file from [here](https://chromedriver.chromium.org/). Unzip and add the "chromedriver.exe" (Windows) or "chromedriver" (Linux) file to the PYTHONPATH environment variable.

    Well, we know that's a lot of work, so we have included the current stable version of the chromedriver in the [dependencies](https://github.com/suhasrsharma/FluffyPancakes/tree/master/dependencies) folder of the repo.

    **You're all set to go.** Although, if, by any chance, you face an issue, just add to PYTHONPATH, the directory structure to where you downloaded this repository.

# Development

Want to contribute? Great!

FluffyPancakes uses http requests, bs4, selenium, and of course, Machine Learning, and a lot more libraries. 
You can find the GitHub repository [here](https://github.com/suhasrsharma/FluffyPancakes).

Make sure to use the following command to get the exact versions of pytest and check-manifest:
```sh
$ pip install -e .[dev]
```

# Development Status
##### Development Status :: 4 - Beta
##### Version - 0.1.1

# License
### MIT
##### Free software? Of Course!

---

In collaboration with the [ISFCR Lab](https://research.pes.edu/isfcr/) at [PES University](https://www.pes.edu/), Bangalore, India.
# McViewer Documentation

## Wiki Link

* For further explanation of the features of this project, check out the [project wiki](https://github.com/chadspector/McViewer/wiki). 

## Development Process

My development process began figuring out how to configure Heroku with my project. After that was completed I went on to brainstorm quickly about what models I would need to write for the site. Models are Python objects that define the structure of an application's data, and provide mechanisms to manage (add, modify, delete) and query records in the database. Once I had written out the models.py file, I went on the implement the different pages I would need.  
One by one, I would write a URL path in the urls.py file and then I would write the view method in views.py which would render each of the specified paths. A URL mapper is used to redirect HTTP requests to the appropriate view based on the request URL. The URL mapper can also match particular patterns of strings or digits that appear in a URL and pass these to a view function as data. A view is a request handler function, which receives HTTP requests and returns HTTP responses. Views access the data needed to satisfy requests via models, and delegate the formatting of the response to templates. In those methods, the entire backend logic of the system is implemented.

## Challenges Faced


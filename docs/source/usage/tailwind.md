

### TODO WRITE DOCS FOR TAILWIND
### STUB

*New in 0.8.0*

Tailwind is now used as the primary CSS framework for the project. Tailwind is a utility-first CSS framework that provides a set of utility classes to style your HTML elements. This allows you to build complex layouts and designs without writing custom CSS.

This added a new dependancy `django-tailwind` to the project.  This require the creation of an additional app `theme` to hold the tailwind configuration and templates. This will be added to the cookiecutter project.

Tailwind requires an additional long running command to watch for changes to the CSS files and recompile them. This is done by running the following command in a terminal window:

```bash
python manage.py tailwind start
```

This will start the Tailwind CSS compiler and watch for changes to the CSS files. You can now start the development server and view the changes in the browser.

Inital setup will require the theme app to be initalized by NPM. This is done by running the following command in the terminal:

```bash
cd theme
npm install
```

This will require Node.js to be installed on your system. You can download Node.js from the official website: [https://nodejs.org/](https://nodejs.org/)

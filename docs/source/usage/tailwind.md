# Tailwind CSS Integration

This document explains how to use Tailwind CSS in the framework with the preconfigured [django-tailwind](https://github.com/timonweb/django-tailwind) package. This integration ensures a seamless workflow for styling your application using Tailwind CSS.

---

## Prerequisites

The framework automatically includes Tailwind CSS through a Django app called `theme`. This app is pre-configured in the `INSTALLED_APPS` of `settings.py`, but it must be initialized before use.

---

## Initialization

To initialize the Tailwind setup, follow these steps:

### 1. Install Tailwind Dependencies
Navigate to the `theme` app directory:
```bash
cd theme
```

Install the required dependencies using npm:
```bash
npm install
```

### 2. Initialize Tailwind
Run the `tailwind init` command to ensure the environment is correctly set up:
```bash
python manage.py tailwind init
```

This command generates the `tailwind.config.js` file and sets up the necessary Tailwind build pipeline.

### 3. Start the Tailwind Development Server
To enable live updates for your styles, start the Tailwind development server:
```bash
python manage.py tailwind start
```

---

## Customizing Tailwind

The `theme` app includes a `tailwind.config.js` file where you can configure your Tailwind setup. Common customizations include:

### 1. Extend the Theme
Add custom colors, fonts, or spacing to your project:
```javascript
module.exports = {
    theme: {
        extend: {
            colors: {
                primary: '#1D4ED8',
                secondary: '#9333EA',
            },
        },
    },
    plugins: [],
};
```

### 2. Enable Dark Mode
To enable dark mode, update your configuration:
```javascript
module.exports = {
    darkMode: 'class', // Use 'media' for system preferences
    theme: {
        extend: {},
    },
};
```

---

## Usage in Templates

Once Tailwind is configured and running, you can use its utility classes directly in your Django templates.

### Example: Buttons
```html
<button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
    Click Me
</button>
```

### Example: Forms
```html
<input type="text" class="block w-full border-gray-200 rounded-lg p-2" placeholder="Enter text">
```

### Example: Tables
```html
<table class="min-w-full divide-y divide-gray-200">
    <thead>
        <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="px-6 py-4 whitespace-nowrap">Example</td>
        </tr>
    </tbody>
</table>
```

---

## Building Tailwind for Production

When deploying your application, you need to compile your CSS for production to reduce file size:

1. Run the following command to build the optimized CSS:
   ```bash
   python manage.py tailwind build
   ```

2. The generated CSS file will be placed in the `static/css` directory and can be served in your production environment.

---

## Troubleshooting

### Styles Not Applied
- Ensure the `theme` app is in `INSTALLED_APPS`.
- Verify the Tailwind development server is running if testing locally.

### Live Updates Not Working
- Confirm you’ve run `python manage.py tailwind start` in the `theme` directory.


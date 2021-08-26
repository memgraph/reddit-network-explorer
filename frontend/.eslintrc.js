module.exports = {
  'root': true,
  'env': {
    'browser': true,
    'es6': true,
  },
  parserOptions: {
    ecmaVersion: 2020,
  },
  overrides: [
    {
      files: ["*.ts"],
      'extends': [
        'google',
        'eslint:recommended',
        'plugin:@typescript-eslint/eslint-recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:prettier/recommended',
        "plugin:@angular-eslint/template/process-inline-templates"
      ],
      'globals': {
        'Atomics': 'readonly',
        'SharedArrayBuffer': 'readonly',
      },
      'parser': '@typescript-eslint/parser',
      'parserOptions': {
        'ecmaVersion': 2018,
        'sourceType': 'module',
      },
      'plugins': [
        '@typescript-eslint',
        'prettier'
      ],
      'rules': {
        'prettier/prettier': [
          'error',
          {
            'singleQuote': true,
            'trailingComma': 'all',
            'printWidth': 120,
          },
        ],
        'max-len': [
          'error',
          {
            'code': 120,
            'ignoreUrls': true,
            'ignorePattern': '^import [^,]+ from |^export | implements ',
          },
        ],
        'no-invalid-this': ['off'],
        'brace-style': ['error', '1tbs'],
        'curly': ['error', 'all'],
        'eqeqeq': ['warn', 'smart'],
        'new-cap': 'off',
        'require-jsdoc': 'off',
        'valid-jsdoc': 'off',
        '@typescript-eslint/no-var-requires': 'off',
        '@typescript-eslint/no-unused-vars': ['error', { args: 'none' }],
        '@typescript-eslint/no-explicit-any': 'off',
        '@typescript-eslint/explicit-function-return-type': 'off',
        '@typescript-eslint/ban-ts-ignore': 'off',
        '@typescript-eslint/no-use-before-define': 'off',
        '@typescript-eslint/ban-types': 'off',
        '@typescript-eslint/explicit-module-boundary-types': 'off',
      },
    },
    {
      files: ["*.component.html"],
      extends: ["plugin:@angular-eslint/template/recommended"],
      rules: {
        '@angular-eslint/template/no-negated-async': 'off',
      }
    }
  ],
};

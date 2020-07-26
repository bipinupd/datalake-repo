Directory Structure 
```
.
├── Readme.md
├── cloudbuild-deploy.yaml
├── cloudbuild.yaml
├── deIdentify-templates
│   └── generic_deidentify_template.json
├── inspect-templates
│   └── inspect_template.json
├── scripts
│   ├── deidentify_script.sh
│   ├── inspect_script.sh
│   └── package.sh
└── tests
    ├── conftest.py
    ├── it-test
    │   ├── generic_deidentify_template_test.py
    │   └── inspect_template_test.py
    ├── pytest.ini
    ├── requirements.txt
    ├── unittest
    │   └── dlp_test.py
    └── utils
        └── common.py
````

Add your DeIdentify templates (`deIdentify-templates`) and the corresponding tests in `tests/it-test`. Make sure the name of the test file corresponds to the name of the template. For example if the name of the template is `generic_deidentify_template.json`, the it-test for this should be `generic_deidentify_template_test.py`. This will help to pick the iteration test file to the related deIdentify-templates. Similarly, perform the similar naming conventions to inspect-templates.

The unit test makes sure there is no conflict in the templates name between different json files. It also makes sure the JSON syntax is correct.


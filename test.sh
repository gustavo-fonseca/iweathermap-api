#!/bin/sh

coverage erase
coverage run manage.py test
coverage report
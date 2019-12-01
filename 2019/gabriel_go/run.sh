#!/bin/bash

set -e

DAY=$1

go run src/day$DAY/${DAY}.go
go run src/day$DAY/${DAY}.2.go

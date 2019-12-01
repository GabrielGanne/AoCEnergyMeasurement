package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
)

func get_fuel(mass int) int {
    return mass / 3 - 2
}

func main() {
    sum := 0

    file, err := os.Open("input")
    if err != nil {
        os.Exit(1)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        mass, err := strconv.Atoi(scanner.Text())
        if err != nil {
             os.Exit(1)
        }
        sum += get_fuel(mass)
    }

    if err := scanner.Err(); err != nil {
        os.Exit(1)
    }

    fmt.Println(sum)
}


package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
)


func to_int(s []string) []int {
	rv := []int{}
	for i := range s {
		v, err := strconv.Atoi(s[i])
		if err != nil {
			os.Exit(1)
		}
		rv = append(rv, v)
	}

	return rv
}

func process(s []int) int {
	i := 0
	last := 0

	for true {
		switch s[i] {
			case 1:
				// add
				last = s[s[i + 1]] + s[s[i + 2]]
				s[s[i + 3]] = last
			case 2:
				// multiply
				last = s[s[i + 1]] * s[s[i + 2]]
				s[s[i + 3]] = last
			case 99:
				// program is finished and should immediately halt
				return s[0]
			default:
				fmt.Println("Error")
				os.Exit(1)
		}

		// fmt.Println(last)

		// move to the next one by stepping forward 4 positions
		i += 4
	}

    return -1;
}


func main() {
    file, err := os.Open("input")
    if err != nil {
        os.Exit(1)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        input := scanner.Text()
        input_slice_str := strings.Split(input, ",")

		for i := 0; i < 100; i++ {
			for j := 0; j < 100; j++ {
				// replace && init
				input_slice := to_int(input_slice_str)
				input_slice[1] = i
				input_slice[2] = j

				rv := process(input_slice)

				if rv == 19690720 {
					fmt.Println(i, j)
					os.Exit(0)
				}
			}
		}
    }

	os.Exit(1)
}


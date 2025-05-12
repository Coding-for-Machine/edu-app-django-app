package main

import (
	"encoding/json"
	"fmt"
)

type User struct {
	Id   int    `json:"id"`
	Name string `json:"name"`
	Age  uint   `json:"age"`
	Addres
}

type Addres struct {
	City string `json:"city"`
}

func (u *User) UserUpdate(newName string) {
	u.Name = newName
}

func main() {
	user1 := User{
		Id:   1,
		Name: "Asadbek",
		Age:  23,
		Addres: Addres{
			City: "Samarqand",
		},
	}
	jsonData, err := json.MarshalIndent(user1, "", "")
	if err != nil {
		fmt.Println("Error")
		return
	}
	fmt.Println(string(jsonData))
	user1.UserUpdate("Kamron")
	fmt.Println(user1)
}

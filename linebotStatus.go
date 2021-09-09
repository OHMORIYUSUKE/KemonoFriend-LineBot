package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
  "os"
  "strings"
  "log"
)

func main() {
  url := os.Getenv("WEBHOOK_URL")

  resp, _ := http.Get(url)
  defer resp.Body.Close()

  byteArray, _ := ioutil.ReadAll(resp.Body)

  //-------------------------------------
  f, err := os.Open("README.md")
    if err != nil{
        fmt.Println("error")
    }
    defer f.Close()

    // 一気に全部読み取り
    b, err := ioutil.ReadAll(f)
    // 出力
    //fmt.Println(string(b))
  //-------------------------------------

  if string(byteArray) == "hello world!" {
	fmt.Println("OK");
    
	replacedMd := strings.Replace(string(b), "## 現在、利用できません。サーバーでエラーが生じています。:weary:", "## 現在、利用できます。:smile:", 1)
	//fmt.Println(replacedMd)

	file, err := os.Create("README.md")
    if err != nil {
        log.Fatal(err)  //ファイルが開けなかったときエラー出力
    }
    defer file.Close()

    file.Write(([]byte)(replacedMd))

  } else {
	fmt.Println("error"); 

	replacedMd := strings.Replace(string(b), "## 現在、利用できます。:smile:", "## 現在、利用できません。サーバーでエラーが生じています。:weary:", 1)
	//fmt.Println(replacedMd)

	file, err := os.Create("README.md")
    if err != nil {
        log.Fatal(err)  //ファイルが開けなかったときエラー出力
    }
    defer file.Close()

    file.Write(([]byte)(replacedMd))
  }
}
package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
  "os"
  "regexp"
  "strings"
  "log"
)

func main() {
  url := os.Getenv("HEROKU_URL")

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
      
    str := []byte(string(b))
    assigned := regexp.MustCompile("<!--status-->\n\n(.*)\n\n<!--status-->")
    group := assigned.FindSubmatch(str)
    fmt.Println(string(group[1]))

    replacedMd := strings.Replace(string(b), string(group[1]), "## 現在、利用できます。:smile:", 1)
    //fmt.Println(replacedMd)
  
    file, err := os.Create("README.md")
      if err != nil {
          log.Fatal(err)  //ファイルが開けなかったときエラー出力
      }
      defer file.Close()
  
      file.Write(([]byte)(replacedMd))
  

  } else {
    fmt.Println("error"); 
    str := []byte(string(b))
    assigned := regexp.MustCompile("<!--status-->\n\n(.*)\n\n<!--status-->")
    group := assigned.FindSubmatch(str)
    fmt.Println(string(group[1]))

    replacedMd := strings.Replace(string(b), string(group[1]), "## 現在、利用できません。サーバーでエラーが生じています。:weary:", 1)
    //fmt.Println(replacedMd)
  
    file, err := os.Create("README.md")
      if err != nil {
          log.Fatal(err)  //ファイルが開けなかったときエラー出力
      }
      defer file.Close()
  
      file.Write(([]byte)(replacedMd))
  }
}
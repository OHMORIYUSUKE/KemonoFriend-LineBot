package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
  "os"
  "regexp"
  "strings"
  "log"
  "time"
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

    b, err := ioutil.ReadAll(f)
  //-------------------------------------
  now := time.Now()
    fmt.Println(now.Format(time.RFC3339))

    nowUTC := now.UTC() 
    fmt.Println(nowUTC.Format(time.RFC3339))

  jst := time.FixedZone("Asia/Tokyo", 9*60*60)

    nowJST := nowUTC.In(jst)                        
    fmt.Println(nowJST.Format(time.RFC3339))
  //-------------------------------------

  if string(byteArray) == "hello world!" {
    fmt.Println("OK");
      
    str := []byte(string(b))
    assigned := regexp.MustCompile("<!--status-->\r\n\r\n(.*)\r\n\r\n<!--status-->")
    group := assigned.FindSubmatch(str)
    fmt.Println(string(group[1]))

    replacedMd := strings.Replace(string(b), string(group[1]), "## 現在、利用できます。:smile:"+nowJST.Format(time.RFC3339)+"現在", 1)
    //fmt.Println(replacedMd)
  
    file, err := os.Create("README.md")
      if err != nil {
          log.Fatal(err) 
      }
      defer file.Close()
  
      file.Write(([]byte)(replacedMd))
  

  } else {
    fmt.Println("error"); 
    str := []byte(string(b))
    assigned := regexp.MustCompile("<!--status-->\r\n\r\n(.*)\r\n\r\n<!--status-->")
    group := assigned.FindSubmatch(str)
    fmt.Println(string(group[1]))

    replacedMd := strings.Replace(string(b), string(group[1]), "## 現在、利用できません。サーバーでエラーが生じています。:weary:"+nowJST.Format(time.RFC3339)+"現在", 1)
  
    file, err := os.Create("README.md")
      if err != nil {
          log.Fatal(err) 
      }
      defer file.Close()
  
      file.Write(([]byte)(replacedMd))
  }
}
package main

import (

  "fmt"
  "crypto/rand"
  "crypto/sha256"
  "os"
  "crypto/aes"
  "encoding/hex"
  "io"
  "bytes"
  "crypto/cipher"
  "bufio"
)


const(
  Line string ="\t----------------------Golang Style------------------------------"
)

//=================================Точка входа
func main(){


  var session_key =SessionKey(20)
  fmt.Println("\n\tСоздаю Сеансовый ключ => ", session_key)
  fmt.Println(Line)

  //=========Сообщение
  var msg =`Блокчейн - это непрерывная цепочка блоков (односвязный список),
  имеющая лишь две операции: чтение и добавление, исключая при этом
  функции редактирования и удаления за счёт элементов криптографии и
  компьютерных сетей.`

  var encrypt_message =Encrypt(HashSum(session_key),msg,true)

  fmt.Println("\tПолучаю Зашифрование Хешированое Сообщение Сеансовым ключем => ",encrypt_message)

  Pause()
}
//**********************************Функции Проекта**********************************

//================= Функции Генерации Сеансового Ключа
func SessionKey(max int)[]byte{
  /*  Принимает один Параметр-Числовое Значение(Размер) ключа
      целочисленное значение(INT)
      Возвращает массив байт
  */
	var slice []byte =make([]byte, max)
	_,err:=rand.Read(slice)

	if err !=nil {return nil}

	for max =max-1;max >=0; max --{
		slice[max] =slice[max]%94 +33
	}

	return slice
}

//==================== Блок AES шифрование Начало===============
func EncryptAES(data, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {panic(err)}
		
	blockSize := block.BlockSize()
	data = PKCS5Padding(data, blockSize)
	cipherText := make([]byte, blockSize + len(data))
	iv := cipherText[:blockSize]
	if _, err := io.ReadFull(rand.Reader, iv); err != nil{panic(err)}
		
	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(cipherText[blockSize:], data)

	return cipherText, nil
}

func PKCS5Padding(ciphertext []byte, blockSize int) []byte {
	padding := blockSize - len(ciphertext) % blockSize
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	return append(ciphertext, padtext...)
}
//-----------------------криптографическая хеш-функция
func  HashSum(data []byte)[]byte{
	var hashed =sha256.Sum256(data)
	return hashed[:]
}
//----------------Главная Функция Шифрование с переводом байтов в строку
func Encrypt(session_key []byte, data string,mode bool) string {
  /*Первый Параметр-Сеансовый Ключ в виде массива байт
   Второй Параметр-Сообщение в виде строки
   возвращает зашифровное соотношение в виде строки
  */
	result, _ := EncryptAES(
		[]byte(data),
		session_key,
	)
  //-----------------Если mode==true,то записать сообщение в файл
  if mode {Write_File_Text(hex.EncodeToString(result))}
  return hex.EncodeToString(result)

}
//====================Блок AES-CBC шифрование Конец===============

//==================Функция Обработки Ошибок================
func CheckError(err error) {
	if err !=nil{
		fmt.Println("\n\t[Error]Возникла Ошибка!", err)
		os.Exit(1)
	}
}
//==================Функция Создание текстового файла===========
func Write_File_Text(data string){
    file,err := os.Create("message.txt")

    CheckError(err)

    defer file.Close()
    file.WriteString(data)

}

//====================Функция Паузы() ====================
func Pause(){
  reader := bufio.NewReader(os.Stdin)
  input, _ := reader.ReadString('\n')
  fmt.Printf(string([]byte(input)[0]))
}

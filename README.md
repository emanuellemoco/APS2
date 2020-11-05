
# Megadados2020-2-Repositório de APS  
Emanuelle Moço e Leonardo Mendes  

---

### APS3  

Estamos utilizando o sistema operacional Manjaro - Linux, onde o mySQL é disponibilizado através do MariaDB.
Algumas funcionalidades do mySQL tradicional não estáo presentes no MariaDB. Esse é o caso das funções ```BIIN_TO_UUID()``` e  ```UUID_TO_BIN()``` que são necessárias para o projeto. 
Para contornar essas limitações, encontramos a implementação manual dessas funções no [GitHub Gist](https://gist.github.com/jamesgmarks/56502e46e29a9576b0f5afea3a0f595c). Para que o projeto funcione nornalmemente para usuários do MariaDB, é necessário rodar o script ```mariaUUID.sql``` que pode ser encontrado em  [APS3/tasklist/database/scripts/](https://github.com/emanuellemoco/APS_Megadados/blob/master/APS3/tasklist/database/scripts/)

Para executar o serviço rode
```
uvicorn tasklist.main:app --reload
```

Para executar os testes rode
```
pytest
```

---
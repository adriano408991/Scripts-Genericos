const express = require('express');    
const bodyParser = require('body-parser');
var sql = require('mssql/msnodesqlv8');

var connStr = {
    driver: 'msnodesqlv8',
    connectionString: 'Driver={SQL Server Native Client 11.0};Server=(local);Database=BancoPrincipal;Trusted_Connection={Yes};',
};
const port = 3000; //porta padrão
const app = express();     

//configurando o body parser para pegar POSTS
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//definindo as rotas
const router = express.Router();
router.get('/', (req, res) => res.json({ message: 'Funcionando!' }));
app.use('/', router);


//teste de conexao
// sql.connect(connStr)
//     .then(conn => console.log("conectou!"))
//     .catch(err => console.log("erro! " + err));

//fazendo a conexão global
sql.connect(connStr)
   .then(conn => global.conn = conn)
   .catch(err => console.log(err));



//funcao para executar sqlQuery
function execSQLQuery(sqlQry, res){
    global.conn.request()
               .query(sqlQry)
               .then(result => res.json(result.recordset))
               .catch(err => res.json(err));
}


// select 
router.get('/clientes', (req, res) =>{
    execSQLQuery('SELECT * FROM Clientes', res);
})


// select outra instancia
router.get('/clientes2', (req, res) =>{
    execSQLQuery('SELECT * FROM  [BancoSecundario].[dbo].[teste]', res);
})



//select by id
router.get('/clientes/:id?', (req, res) =>{
    let filter = '';
    if(req.params.id) filter = ' WHERE ID=' + parseInt(req.params.id);
    execSQLQuery('SELECT * FROM Clientes' + filter, res);
})

//delete
router.delete('/clientes/:id', (req, res) =>{
    execSQLQuery('DELETE Clientes WHERE ID=' + parseInt(req.params.id), res);
})

//insert
router.post('/clientes', (req, res) =>{    
    const nome = req.body.nome.substring(0,150);
    const cpf = req.body.cpf.substring(0,11);
    execSQLQuery(`INSERT INTO Clientes(Nome, CPF) VALUES('${nome}','${cpf}')`, res.json({message:"foi"}));    
})

//atualiza
router.patch('/clientes/:id', (req, res) =>{
    const id = parseInt(req.params.id);
    const nome = req.body.nome.substring(0,150);
    const cpf = req.body.cpf.substring(0,11);
    execSQLQuery(`UPDATE Clientes SET Nome='${nome}', CPF='${cpf}' WHERE ID=${id}`, res);
})


//inicia o servidor
app.listen(port);
console.log('API funcionando!');

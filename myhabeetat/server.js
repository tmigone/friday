const express = require('express')
const MyHabeetat = require('myhabeetat')
const bodyParser = require('body-parser')

const PORT = 8080
const app = express()
app.use(bodyParser.urlencoded({ extended: false }))

// LOGIN
app.post('/login', async (req,res) => {
  try {
    let token = await MyHabeetat.login(req.body.email, req.body.password)
    res.json({ status: 'ok', token: token })
  } catch (error) {
    res.json({ status: 'error', message: error.message })
  }
})

// DEVICES
app.post('/devices', async (req,res) => {
  try {
    let devices = await MyHabeetat.getDevices(req.body.token, req.body.home)
    res.json({ status: 'ok', devices: devices })
  } catch (error) {
    res.json({ status: 'error', message: error.message })
  }
})

// HOMES
app.post('/homes', async (req,res) => {
  try {
    let homes = await MyHabeetat.getHomes(req.body.token)
    res.json({ status: 'ok', homes: homes })
  } catch (error) {
    res.json({ status: 'error', message: error.message })
  }
})

// STATUS
app.post('/status', async (req,res) => {
  try {
    let status = await MyHabeetat.getDeviceStatus(req.body.token, parseInt(req.body.home), parseInt(req.body.device))
    res.json({ status: 'ok', devices: status })
  } catch (error) {
    res.json({ status: 'error', message: error.message })
  }
})

// SET
app.post('/set', async (req,res) => {
  try {
    let status = {}
    if (req.body.mode) status.mode = req.body.mode
    if (req.body.fanMode) status.fanMode = req.body.fanMode
    if (req.body.targetTemperature) status.targetTemperature = req.body.targetTemperature
    let result = await MyHabeetat.setDeviceStatus(req.body.token, parseInt(req.body.model), parseInt(req.body.endpoint), status)
    res.json({ status: 'ok', devices: result })
  } catch (error) {
    res.json({ status: 'error', message: error.message })
  }
})



app.listen(PORT)
console.log(`Running MyHabeetat API on port ${PORT}`)
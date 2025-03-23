package com.example.radhikachatbot

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.radhikachatbot.ui.theme.RadhikaChatBotTheme
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.IOException

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            RadhikaChatBotTheme {
                ChatScreen()
            }
        }
    }
}

@Composable
fun ChatScreen() {
    val messages = remember { mutableStateListOf<Message>() }
    var userInput by remember { mutableStateOf(TextFieldValue("")) }
    val coroutineScope = rememberCoroutineScope()
    val listState = rememberLazyListState()
    val isTyping = remember { mutableStateOf(false) }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        bottomBar = {
            Column {
                if (isTyping.value) {
                    Text(
                        text = "Radhika is typing...",
                        modifier = Modifier.padding(start = 16.dp, bottom = 4.dp),
                        color = Color.Gray
                    )
                }
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(10.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    TextField(
                        value = userInput,
                        onValueChange = { userInput = it },
                        placeholder = { Text("Type a message...") },
                        modifier = Modifier
                            .weight(1f)
                            .padding(8.dp),
                        keyboardOptions = KeyboardOptions.Default.copy(
                            imeAction = ImeAction.Send
                        ),
                        keyboardActions = KeyboardActions(
                            onSend = {
                                sendMessage(userInput.text, messages, coroutineScope, listState, isTyping)
                                userInput = TextFieldValue("") // ✅ Clear input after sending
                            }
                        )
                    )
                    Button(
                        onClick = {
                            sendMessage(userInput.text, messages, coroutineScope, listState, isTyping)
                            userInput = TextFieldValue("") // ✅ Clear input
                        },
                        modifier = Modifier.padding(start = 8.dp)
                    ) {
                        Text("Send")
                    }
                }
            }
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues),
            state = listState
        ) {
            items(messages) { message ->
                AnimatedChatBubble(message)
            }
        }
    }
}

@Composable
fun AnimatedChatBubble(message: Message) {
    val isUser = message.sender == "You"

    AnimatedVisibility(
        visible = true,
        enter = fadeIn(animationSpec = tween(300)) + slideInHorizontally(),
        exit = fadeOut(animationSpec = tween(300)) + slideOutHorizontally()
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp),
            contentAlignment = if (isUser) Alignment.CenterEnd else Alignment.CenterStart
        ) {
            Column(
                modifier = Modifier
                    .background(
                        color = if (isUser) Color(0xFF81C784) else Color(0xFFBBDEFB),
                        shape = RoundedCornerShape(12.dp)
                    )
                    .padding(12.dp)
            ) {
                Text(
                    text = "${message.sender}: ${message.text}",
                    color = Color.Black
                )
            }
        }
    }
}

data class Message(val sender: String, val text: String)

fun sendMessage(
    userMessage: String,
    messages: MutableList<Message>,
    coroutineScope: CoroutineScope,
    listState: LazyListState,
    isTyping: MutableState<Boolean>
) {
    if (userMessage.isBlank()) return

    messages.add(Message("You", userMessage))

    coroutineScope.launch {
        listState.animateScrollToItem(messages.size - 1) // ✅ Auto-scroll
        isTyping.value = true // ✅ Show "Radhika is typing..."
        delay(1000) // ✅ Simulate typing delay
        sendMessageToServer(userMessage, messages, isTyping)
    }
}

fun sendMessageToServer(userMessage: String, messages: MutableList<Message>, isTyping: MutableState<Boolean>) {
    val client = OkHttpClient()

    val json = JSONObject().put("message", userMessage).toString()
    val mediaType = "application/json; charset=utf-8".toMediaType()
    val requestBody = json.toRequestBody(mediaType)

    val request = Request.Builder()
        .url("http://192.168.1.26:5000/chat") // ✅ Replace with your actual IP
        .post(requestBody)
        .build()

    client.newCall(request).enqueue(object : Callback {
        override fun onFailure(call: Call, e: IOException) {
            messages.add(Message("Radhika", "Oops! Kuch kaam Yaad aa gya he baad mei baat krti hu ! 😢"))
            isTyping.value = false
        }

        override fun onResponse(call: Call, response: Response) {
            val body = response.body
            body?.let { responseBody ->
                val responseText = JSONObject(responseBody.string()).getString("response")
                messages.add(Message("Radhika", responseText))
            }
            isTyping.value = false
        }
    })
}

@Preview(showBackground = true)
@Composable
fun ChatScreenPreview() {
    RadhikaChatBotTheme {
        ChatScreen()
    }
}

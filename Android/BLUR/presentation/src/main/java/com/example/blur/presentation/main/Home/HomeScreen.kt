package com.example.blur.presentation.main.Home

import android.content.Intent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.forEachGesture
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Widgets
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.blur.presentation.R
import com.example.blur.presentation.component.ListItems
import com.example.blur.presentation.main.Home.CameraX.CameraXActivity

@OptIn(ExperimentalMaterial3Api::class, ExperimentalComposeUiApi::class)
@Composable
fun HomeScreen() {
    val scrollState = rememberScrollState()
    val context = LocalContext.current
    // FocusRequester 인스턴스 생성
    val keyboardController = LocalSoftwareKeyboardController.current
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp)
            .background(MaterialTheme.colorScheme.background)
            .verticalScroll(scrollState)
            .pointerInput(Unit) {
                forEachGesture {
                    awaitPointerEventScope {
                        awaitFirstDown().also {
                            keyboardController?.hide()
                        }
                    }
                }
            }
    ) {

        Image(
            painter = painterResource(id = R.drawable.logo_m),
            contentDescription = null,
            modifier = Modifier
                .width(80.dp)
                .heightIn(120.dp)
        )

        Spacer(modifier = Modifier.height(40.dp))


        ListItems(
            headlineText = "얼굴 등록",
            supportingText = "나의 사진을 찍어서 기기에 얼굴을 등록해보세요",
            icon = Icons.Filled.Person,
            onClick = {
                context.startActivity(Intent(context, CameraXActivity::class.java))
            }
        )
        Spacer(modifier = Modifier.height(8.dp))

        ListItems(
            headlineText = "위젯 설정",
            supportingText = "스마트 미러의 위젯을 설정해보세요.",
            icon = Icons.Filled.Widgets,
            onClick = {
            }
        )

    }
}

@Preview
@Composable
fun HomeScreenPreview() {
    HomeScreen()
}
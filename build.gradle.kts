plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}

android {
    namespace = "com.example.radhikachatbot"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.radhikachatbot"
        minSdk = 29
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17  // 🔹 Updated to Java 17 (Recommended)
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"  // 🔹 Match Java version
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    // ✅ Core Dependencies
    implementation("androidx.core:core-ktx:1.12.0") // Latest Core KTX
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.6.2") // Lifecycle KTX
    implementation("androidx.activity:activity-compose:1.8.0") // Latest Activity Compose

    // ✅ Jetpack Compose BOM (Manages all Compose versions automatically)
    implementation(platform("androidx.compose:compose-bom:2023.10.01"))
    implementation("androidx.compose.ui:ui") // UI Components
    implementation("androidx.compose.ui:ui-tooling-preview") // Preview Support
    implementation("androidx.compose.ui:ui-graphics") // UI Graphics
    implementation("androidx.compose.foundation:foundation") // Foundation Components
    implementation("androidx.compose.material3:material3") // Material 3
    implementation("androidx.compose.runtime:runtime-livedata") // LiveData Support

    // ✅ Fix for `LocalSoftwareKeyboardController`
    implementation("androidx.compose.ui:ui-text") // Text Input Support

    // ✅ Networking (OkHttp for API Calls)
    implementation("com.squareup.okhttp3:okhttp:4.12.0") // Latest OkHttp

    // ✅ Coroutines for Asynchronous Tasks
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3") // Latest Coroutines

    // ✅ Testing Dependencies
    testImplementation("junit:junit:4.13.2") // Unit Testing
    androidTestImplementation("androidx.test.ext:junit:1.1.5") // Android JUnit
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1") // Espresso UI Testing
    androidTestImplementation("androidx.compose.ui:ui-test-junit4") // Compose UI Testing
    debugImplementation("androidx.compose.ui:ui-tooling") // Debugging & Previews
    debugImplementation("androidx.compose.ui:ui-test-manifest") // Test Manifest
}

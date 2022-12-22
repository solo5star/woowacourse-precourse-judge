plugins {
    kotlin("jvm") version "1.6.21"
}

repositories {
    mavenCentral()
    maven { setUrl("https://jitpack.io") }
}

dependencies {
    implementation("com.github.woowacourse-projects:mission-utils:1.0.0")
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(11))
    }
}

tasks {
    test {
        useJUnitPlatform()
    }
}

// https://gist.github.com/matthiasbalke/3c9ecccbea1d460ee4c3fbc5843ede4a
tasks.register<Task>(name = "resolveDependencies") {
    group = "Build Setup"
    description = "Resolve and prefetch dependencies"
    doLast {
        rootProject.allprojects.forEach {
            it.buildscript.configurations.filter(Configuration::isCanBeResolved).forEach { it.resolve() }
            it.configurations.filter(Configuration::isCanBeResolved).forEach { it.resolve() }
        }
    }
}

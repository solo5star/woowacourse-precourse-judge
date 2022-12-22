package menu

import camp.nextstep.edu.missionutils.Randoms
import camp.nextstep.edu.missionutils.test.NsTest
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Assertions.assertTimeoutPreemptively
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Nested
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.function.Executable
import org.mockito.ArgumentMatchers
import org.mockito.MockedStatic
import org.mockito.Mockito.mockStatic
import java.time.Duration
import java.util.Arrays


class ApplicationTest : NsTest() {
    @DisplayName("전체 기능 테스트")
    @Nested
    internal inner class AllFeatureTest {
        @Test
        fun `기능 테스트`() {
            assertTimeoutPreemptively(RANDOM_TEST_TIMEOUT) {
                val executable = Executable {
                    runException("구구,제임스", "김밥", "떡볶이")
                    assertThat(output()).contains(
                        "점심 메뉴 추천을 시작합니다.",
                        "코치의 이름을 입력해 주세요. (, 로 구분)",
                        "구구(이)가 못 먹는 메뉴를 입력해 주세요.",
                        "제임스(이)가 못 먹는 메뉴를 입력해 주세요.",
                        "메뉴 추천 결과입니다.",
                        "[ 구분 | 월요일 | 화요일 | 수요일 | 목요일 | 금요일 ]",
                        "[ 카테고리 | 한식 | 양식 | 일식 | 중식 | 아시안 ]",
                        "[ 구구 | 김치찌개 | 스파게티 | 규동 | 짜장면 | 카오 팟 ]",
                        "[ 제임스 | 제육볶음 | 라자냐 | 가츠동 | 짬뽕 | 파인애플 볶음밥 ]",
                        "추천을 완료했습니다."
                    )
                }
                assertRandomTest(
                    executable,
                    Mocking.ofRandomNumberInRange(2, 5, 1, 3, 4),  // 숫자는 카테고리 번호를 나타낸다.
                    Mocking.ofShuffle(
                        // 월요일
                        listOf("김치찌개", "김밥", "쌈밥", "된장찌개", "비빔밥", "칼국수", "불고기", "떡볶이", "제육볶음"),  // 구구
                        listOf("제육볶음", "김밥", "김치찌개", "쌈밥", "된장찌개", "비빔밥", "칼국수", "불고기", "떡볶이"),  // 제임스
                        // 화요일
                        listOf("스파게티", "라자냐", "그라탱", "뇨끼", "끼슈", "프렌치 토스트", "바게트", "피자", "파니니"),  // 구구
                        listOf("라자냐", "그라탱", "뇨끼", "끼슈", "프렌치 토스트", "바게트", "스파게티", "피자", "파니니"),  // 제임스
                        // 수요일
                        listOf("규동", "우동", "미소시루", "스시", "가츠동", "오니기리", "하이라이스", "라멘", "오코노미야끼"),  // 구구
                        listOf("가츠동", "규동", "우동", "미소시루", "스시", "오니기리", "하이라이스", "라멘", "오코노미야끼"),  // 제임스
                        // 목요일
                        listOf("짜장면", "깐풍기", "볶음면", "동파육", "짬뽕", "마파두부", "탕수육", "토마토 달걀볶음", "고추잡채"),  // 구구
                        listOf("짬뽕", "깐풍기", "볶음면", "동파육", "짜장면", "마파두부", "탕수육", "토마토 달걀볶음", "고추잡채"),  // 제임스
                        // 금요일
                        listOf("카오 팟", "팟타이", "나시고렝", "파인애플 볶음밥", "쌀국수", "똠얌꿍", "반미", "월남쌈", "분짜"),  // 구구
                        listOf("파인애플 볶음밥", "팟타이", "카오 팟", "나시고렝", "쌀국수", "똠얌꿍", "반미", "월남쌈", "분짜") // 제임스
                    )
                )
            }
        }
    }

    class Mocking<T>(
        /**
         * stubbing lambda verification
         * 예시)
         * () -> Randoms.pickNumberInList(anyList())
         */
        private val verification: MockedStatic.Verification,
        // 반환할 첫 번째 값
        private val value: T,
        vararg values: T
    ) {
        /**
         * 첫 번째 값을 반환하고 나서 다음에 반환할 값들.
         * 예를 들면, verification을 처음 실행하면 value를 반환하고
         * 두 번째 실행하면 values[0]을 반환한다.
         */
        private val values: Array<T>

        init {
            this.values = values as Array<T>
        }

        fun <S> stub(mock: MockedStatic<S>) {
            mock.`when`<Any>(verification).thenReturn(value, *Arrays.stream(values).toArray())
        }

        companion object {
            fun ofRandomNumberInRange(value: Int?, vararg values: Int?): Mocking<*> {
                return Mocking<Any?>({
                    Randoms.pickNumberInRange(
                        ArgumentMatchers.anyInt(),
                        ArgumentMatchers.anyInt()
                    )
                }, value, *values)
            }

            fun <T> ofShuffle(value: List<T>?, vararg values: List<T>?): Mocking<*> {
                return Mocking<Any?>({ Randoms.shuffle(ArgumentMatchers.anyList<Any>()) }, value, *values)
            }
        }

    }

    override fun runMain() {
        main()
    }

    companion object {
        private val RANDOM_TEST_TIMEOUT = Duration.ofSeconds(10L)
        private fun assertRandomTest(
            executable: Executable,
            vararg mockingValues: Mocking<*>
        ) {
            assertTimeoutPreemptively(RANDOM_TEST_TIMEOUT) {
                mockStatic(Randoms::class.java).use { mock ->
                    Arrays.stream(mockingValues).forEach { mocking -> mocking.stub(mock) }
                    executable.execute()
                }
            }
        }
    }
}

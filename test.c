#include<stdio.h>

int main() {
    int i;
    float sum = 0.0, average;
    float scores[15];  // ประกาศ array เก็บคะแนนนักเรียน 15 คน

    // รับค่าคะแนนของนักเรียน 15 คน
    for (i = 0; i < 15; i++) {
        printf("Enter score for student %d: ", i + 1);
        scanf("%f", &scores[i]);
        sum += scores[i];  // รวมคะแนนทั้งหมด
    }

    // คำนวณค่าเฉลี่ย
    average = sum / 15;

    // แสดงผลค่าเฉลี่ย
    printf("The average score is: %.2f\n", average);

    return 0;
}


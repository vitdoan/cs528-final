// Code used from https://github.com/nkolban/esp32-snippets/blob/d95258eb6c7a8ec6cd537a80cc2b79aa6435aab3/hardware/accelerometers/mpu6050.c
// One button black 12 red 11, other button black 14 red 13

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"
#include "driver/gpio.h"
#include "sdkconfig.h"
#include "iot_button.h"
#include "esp_log.h"
#include "esp_pm.h"
#include "esp_sleep.h"
#include "esp_idf_version.h"
#include "driver/gpio.h"

#define BUTTON1 4
#define BUTTON2 5
#define BUTTON3 6

void i2c_init()
{
    i2c_config_t i2c_config = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = 0,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_io_num = 1,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = 100000};
    i2c_param_config(I2C_NUM_0, &i2c_config);
    i2c_driver_install(I2C_NUM_0, I2C_MODE_MASTER, 0, 0, 0);

    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (0x68 << 1) | I2C_MASTER_WRITE, 1);
    i2c_master_write_byte(cmd, 0x6B, 1);
    i2c_master_write_byte(cmd, 0, 1);
    i2c_master_stop(cmd);
    i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);
}

void mpu6050_read_data()
{
    uint8_t data[14]; // MPU6050 registers for accelerometer and gyroscope
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (0x68 << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, 0x3B, true);
    i2c_master_stop(cmd);
    i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);

    cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (0x68 << 1) | I2C_MASTER_READ, 1);
    i2c_master_read(cmd, data, sizeof(data), I2C_MASTER_LAST_NACK);
    i2c_master_stop(cmd);
    i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);

    // Process raw data from MPU6050
    int16_t accel_x = (data[0] << 8) | data[1];
    int16_t accel_y = (data[2] << 8) | data[3];
    int16_t accel_z = (data[4] << 8) | data[5];
    int16_t gyro_x = (data[8] << 8) | data[9];
    int16_t gyro_y = (data[10] << 8) | data[11];
    int16_t gyro_z = (data[12] << 8) | data[13];

    printf("%d, %d, %d, %d, %d, %d\n", accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z);
    // printf(">accel_x:%d\n>accel_y:%d\n>accel_z:%d\n>gyro_x:%d\n>gyro_y:%d\n>gyro_z:%d\n", accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z);
}

void button_init(uint32_t button_num, uint32_t button_num2, uint32_t button_num3)
{
    gpio_config_t io_conf;
    // Initialize the GPIO configuration structure
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pin_bit_mask = (1ULL << button_num) | (1ULL << button_num2) | (1ULL << button_num3);
    io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    gpio_config(&io_conf);
}

void app_main()
{
    i2c_init();
    button_init(BUTTON1, BUTTON2, BUTTON3);
    int samples_per_sec = 100;
    int time = 3;

    while (1)
    {
        if (gpio_get_level(BUTTON1) == 1)
        {
            printf("Normal\n");
            for (int i = 0; i < time * samples_per_sec; i++)
            {
                mpu6050_read_data();
                vTaskDelay((1000 / samples_per_sec) / portTICK_PERIOD_MS);
            }
        }
        else if (gpio_get_level(BUTTON2) == 1)
        {
            printf("Changed\n");
            for (int i = 0; i < time * samples_per_sec; i++)
            {
                mpu6050_read_data();
                vTaskDelay((1000 / samples_per_sec) / portTICK_PERIOD_MS);
            }
        }
        else if (gpio_get_level(BUTTON3) == 1)
        {
            printf("Land\n");
            vTaskDelay(1000 / portTICK_PERIOD_MS);
        }
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}
/*
 * File: main.c
 * Author: Matthias Falger
 * Date: November 13, 2023
 * Description: A software task for linux
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>  //Header file for sleep(). man 3 sleep for details. 
#include <time.h>
#include <signal.h>
#include <sys/time.h>
#include <string.h>
#include <errno.h>

/* defines */
#define GET_SCHED_TIME(hours, minutes)((hours*60) + (minutes))
#define NUMBERS_OF_ACTIVITY 8
#define UNDONE 0
#define DONE 1

/* external declarations */

/* typedefs */

/* global variable declarations */
struct Activity {
    char name[50];
    int start_time;
    int stop_time;
    int state;        
};

struct t_eventData{
    int myData;
};

struct Activity activities [NUMBERS_OF_ACTIVITY] = {
    {"going to the Bathroom",   GET_SCHED_TIME(7,0), GET_SCHED_TIME(7,30), UNDONE},   //Activity 1 | 7:00 - 7:30
    {"having Breakfast",        GET_SCHED_TIME(8,0), GET_SCHED_TIME(8,30), UNDONE},   //Activity 2 | 8:00 - 8:30
    {"do some cleaning",        GET_SCHED_TIME(9,0), GET_SCHED_TIME(11,30), UNDONE},  //Activity 3 | 9:00 - 11:30
    {"having lunch",            GET_SCHED_TIME(12,0), GET_SCHED_TIME(12,30), UNDONE}, //Activity 4 | 12:00 - 12:30
    {"napping for a while",     GET_SCHED_TIME(13,0), GET_SCHED_TIME(13,30), UNDONE}, //Activity 5 | 13:00 - 13:30
    {"going for a walk",        GET_SCHED_TIME(15,0), GET_SCHED_TIME(15,30), UNDONE}, //Activity 6 | 15:00 - 15:30
    {"having dinner",           GET_SCHED_TIME(19,0), GET_SCHED_TIME(20,0), UNDONE},  //Activity 7 | 19:00 - 20:30
    {"sleeping",                GET_SCHED_TIME(22,0), GET_SCHED_TIME(23,0), UNDONE},  //Activity 8 | 22:00 - 23:00
}; 

int iglobal_time;

/* function prototypes */
void check_activity_at_time (int time);
void check_activity_now ();
void periodic_timer_callback(union sigval timer_data);



/*
 * Function: main
 * ----------------------------
 * The main function of the program.
 *
 * Parameters:
 *   - argc (int): Number of command-line arguments. One command line argument can be processed
 *   - argv (char *[]): Array of strings representing command-line arguments. The first argument is the speed factor
 *
 * Returns:
 *   - int: Exit status of the program.
 */
int main(int argc, char *argv[]) {
    struct itimerval periodic_timer;
    char str_in[8];
    time_t current_time;
    struct tm *timeinfo;
    int hour, minute;
    int speed_factor;
    int res = 0;
    timer_t timerId = 0;
    struct t_eventData eventData = { .myData = 0 };
    /*  sigevent specifies behaviour on expiration  */
    struct sigevent sev = { 0 };
    /* specify start delay and interval
     * it_value and it_interval must not be zero */
    struct itimerspec its = {   .it_value.tv_sec  = 60,
                                .it_value.tv_nsec = 0,
                                .it_interval.tv_sec  = 60,
                                .it_interval.tv_nsec = 0
                            };    
    sev.sigev_notify = SIGEV_THREAD;
    sev.sigev_notify_function = &periodic_timer_callback;
    sev.sigev_value.sival_ptr = &eventData;

    //Get speed factor from Arguments
    if (2 == argc){
      if (atoi(argv[1]) > 0)
        speed_factor = atoi(argv[1]);
      else
        speed_factor = 1;
    }
    else{
      speed_factor = 1;
    }
    printf("Speed factor: %i \n", speed_factor);

    if (speed_factor < 1){
      its.it_value.tv_sec = 60;
      its.it_interval.tv_sec = 60;
    }
    else if (speed_factor <= 60){
      its.it_value.tv_sec = 60 / speed_factor;
      its.it_interval.tv_sec = 60 / speed_factor;
    }
    else{
      its.it_value.tv_sec = 1;
      its.it_interval.tv_sec = 1;
    }

    /* create timer */
    res = timer_create(CLOCK_REALTIME, &sev, &timerId);

        if (res != 0){
        fprintf(stderr, "Error timer_create: %s\n", strerror(errno));
        exit(-1);
    }

    /* start timer */
    res = timer_settime(timerId, 0, &its, NULL);

    if (res != 0){
        fprintf(stderr, "Error timer_settime: %s\n", strerror(errno));
        exit(-1);
    }

    //get system Time at Program startup
    current_time = time(NULL);
    timeinfo = localtime(&current_time);
    hour = timeinfo-> tm_hour;
    minute = timeinfo->tm_min;
    iglobal_time = GET_SCHED_TIME(hour,minute);

    printf("---- Welcome to the grandma scheduler ----\n");
    printf("---- Current time is %02d:%02d -----------\n", hour, minute);
    if (speed_factor != 1)
      printf("---- Time is running %d times faster than normal \n", speed_factor);

    while(1){
      printf("Enter Time or just wait for your activities \n");
      fgets(str_in, 8, stdin);
      hour = (str_in[0]-'0')*10 + (str_in[1]-'0');
      minute = ((str_in[3]-'0')*10) + str_in[4]-'0';
      //printf("Hour: %i Minute: %i \n", hour, minute);
      if (hour < 0 || hour > 24 || minute < 0 || minute > 60){
        printf("Time not recognized. Please enter formatted time: hh:mm (e.g. 09:05) \n");
      }
      else{
        if ('n'==str_in[0] && 'o'==str_in[1] && 'w'==str_in[2]){
          check_activity_at_time(iglobal_time);
        }
        else{
          check_activity_at_time(GET_SCHED_TIME(hour,minute));
        }
      }
    }

}

/*
 * Function: check_activity_at_time
 * ----------------------------
 * the fuction checks which activity is active and interact with the user.
 *
 * Parameters:
 *    - time: time to be checked
 *
 * Returns:
 *   - 
 */
void check_activity_at_time (int time){
    char str_in[20];

    // Check if an activity is currently pending
    for (int i = 0; i<NUMBERS_OF_ACTIVITY; i++){
        if (activities[i].start_time<=time &&    //Check if activity is pending
            activities[i].stop_time>=time){
            if (UNDONE==activities[i].state){        //Check if state is undone
                printf("Its %s - Time \n", activities[i].name);
                fflush(stdout);
                sleep(3);
                printf("Would you like to %s ? \n", activities[i].name);
                fgets(str_in, 16, stdin);
                if ('y' == str_in[0]){
                    activities[i].state = DONE;
                    printf("Done \n");
                    sleep(3);
                }
                else{
                    printf("%s keeps undone \n", activities[i].name);
                    sleep(3);
                }
            }
            else{ 
                printf("Chill you already done with %s \n", activities[i].name);
                sleep(3);
            }
        }
    }
}

/*
 * Function: check_activity_now
 * ----------------------------
 * the fuction checks if a activity starts or if an activity is ending in 10 minutes
 *
 * Parameters:
 *    -
 *
 * Returns:
 *   - 
 */
void check_activity_now (){
  for (int i = 0; i<NUMBERS_OF_ACTIVITY; i++){
    if (iglobal_time == 0){             // Reset all activity states at the beginning of a new day
      activities[i].state = UNDONE;
    }
    if (activities[i].start_time==iglobal_time){
      printf("Now its time for %s \n", activities[i].name);
    }
    if ((activities[i].stop_time-10)==iglobal_time && UNDONE==activities[i].state){
      printf("Only ten minutes remaining to %s \n", activities[i].name);
    } 
  } 
}

/*
 * Function: periodic_timer_callback
 * ----------------------------
 * this callback will be called every minute or faster (depending on the speed factor)
 *
 * Parameters:
 *    - timer_data: not used
 *
 * Returns:
 *   - 
 */
void periodic_timer_callback(union sigval timer_data)
{
    iglobal_time++;   //Increase the minutes
    check_activity_now ();
    if (iglobal_time > GET_SCHED_TIME(24, 00)){
      iglobal_time = 0;
    }
}

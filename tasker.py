#!/usr/bin/env python3

from argparse import ArgumentParser
import datetime as dt
import colorama
import os.path
from pathlib import Path


TASKS_PATH = str(Path.home()) + "/" + ".tasker_tasks.txt"

PRIORITY = {'1': colorama.Fore.RESET,
			'2': colorama.Fore.LIGHTYELLOW_EX,
			'3': colorama.Fore.LIGHTRED_EX}


def die(error):
	print()
	print("tasker.py: error: " + error)
	exit(1)


def add_arguments(parser):
	parser.add_argument("-a", "--add", action="store_true",
						dest="add", default=False,
						help="add new task to list")
	parser.add_argument("-d", nargs="+", dest="delete",
						help="delete tasks from list")
	parser.add_argument("-l", "--list", action="store_true",
						dest="print", default=False, 
						help="print tasks list")
	parser.add_argument("-t", "--time", action="store_true",
						dest="time", default=False,
						help="add deadline for task")
	parser.add_argument("-q", "--quiet",
	                    action="store_false", dest="verbose", default=True,
	                    help="don't print status messages to stdout")
	# TODO: edit task option


def check_file_exist():
	# create file if not found
	if not os.path.isfile(TASKS_PATH):
		file = open(TASKS_PATH, 'w+')
		file.close()


def read_tasks():
	check_file_exist()

	with open(TASKS_PATH, 'r') as handler:
		tasks = handler.read().strip().split('\n')

	if len(tasks) == 1 and tasks[0] == '':
		print("Your tasks list is empty")
		exit(0)
	return tasks


def print_tasks():
	tasks = read_tasks()
	colorama.init()
	for i, task in enumerate(tasks):
		prior, date, task, deadline = task.split('|')

		if deadline:
			deadline = colorama.Fore.MAGENTA + " (due: " + deadline + ")"
		
		print(PRIORITY['1'] + str(i+1) + "."
			+ colorama.Fore.LIGHTMAGENTA_EX
			+ " (" + date + ") "
			+ PRIORITY[prior] + task
			+ deadline)


def add_new_task(verbose, time):
	if verbose:
		print("Write your task:")
	task = input()

	if task == '':
		die("empty task")
	if '|' in task:
		die("char '|' restricted")

	if verbose:
		print("Set your priority:")
	priority = input()

	if priority.strip() not in ['1', '2', '3']:
		priority = '1'

	date = dt.datetime.now()

	if time:
		if verbose:
			print("Write days to deadline")
		try:
			days = abs(int(input()))
		except ValueError:
			die("invalid integer input")

		days = (date + dt.timedelta(days=days)).strftime("%d.%m.%y")
	else:
		days = ' '

	date = date.strftime("%d.%m.%y")

	with open(TASKS_PATH, 'a') as handler:
		handler.write(priority + '|'
						+ date + '|'
						+ task + '|'
						+ days + '\n')

	if verbose:
		print("Task added successfully")


def delete_task(args):
	tasks = read_tasks()
	tasks_to_delete = sorted(list(map(int, set(args.delete))))[::-1]

	for index in tasks_to_delete:
		index = int(index) - 1
		if index < 0:
			die("index can't be negative number")
		try:
			tasks.pop(index)
		except ValueError:
			die("invalid task index")
		except IndexError:
			die("index is out of range")

	with open(TASKS_PATH, 'w') as handler:
		for task in tasks:
			if task:
				handler.write(task + '\n')

	if args.verbose:
		print("Tasks " + str(tasks_to_delete[::-1]) + " deleted")


def main():
	parser = ArgumentParser(description='Simple task manager')
	add_arguments(parser)
	args = parser.parse_args()

	if args.delete and args.add:
		parser.print_usage()
		die("only one option required")

	if not args.delete and not args.add:
		print_tasks()
		exit(0)
	elif args.add:
		add_new_task(args.verbose, args.time)
	elif args.delete:
		delete_task(args)

	if args.print:
		print_tasks()


if __name__ == "__main__":
	main()
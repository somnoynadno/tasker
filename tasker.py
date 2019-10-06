#!/usr/bin/env python3

from argparse import ArgumentParser
import os.path

TASKS_PATH = "./tasks.txt"

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
	parser.add_argument("-l", "--list",action="store_true",
						dest="print", default=False, 
						help="print tasks list")
	parser.add_argument("-q", "--quiet",
	                    action="store_false", dest="verbose", default=True,
	                    help="don't print status messages to stdout")


def check_file_exist():
	# create file if not found
	if not os.path.isfile(TASKS_PATH):
		with open(TASKS_PATH, 'w'):
			pass


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
	for i, task in enumerate(tasks):
		print(str(i+1) + ". " + task)
		# TODO: add pretty print


def add_new_task(verbose):
	if verbose:
		print("Write your task:")
	task = input()

	# TODO: this
	# if verbose:
	# 	print("Set your priority:")
	# priority = input()

	with open(TASKS_PATH, 'a') as handler:
		handler.write(task + '\n')

	if verbose:
		print("Task added successfully")
	# TODO: add datetime


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
		add_new_task(args.verbose)
	elif args.delete:
		delete_task(args)

	if args.print:
		print_tasks()


if __name__ == "__main__":
	main()
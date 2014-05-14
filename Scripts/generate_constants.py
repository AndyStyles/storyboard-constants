#!/usr/bin/env python

import sys, os
import xml.etree.ElementTree as et

PREFIX = "JBW"

segueIdentifiers = {}
controllerIdentifiers = {}
cellIdentifiers = {}

def addSegueIdentifier(identifier):
	key = identifier[0].upper() + identifier[1:]
	if not key.startswith(PREFIX.upper()):
		key = PREFIX.upper() + key
	
	segueIdentifiers[key] = identifier

def addControllerIdentifier(identifier):
    key = identifier[0].upper() + identifier[1:]
    if not key.startswith(PREFIX.upper()):
        key = PREFIX.upper() + key
    
    controllerIdentifiers[key] = identifier

def addCellIdentifier(identifier):
    key = identifier[0].upper() + identifier[1:]
    if not key.startswith(PREFIX.upper()):
        key = PREFIX.upper() + key
    
    cellIdentifiers[key] = identifier

def process_storyboard(file):
    tree = et.parse(file)
    root = tree.getroot()
    
    for segue in root.iter("segue"):
        segueIdentifier = segue.get("identifier")
        if segueIdentifier == None:
            continue
        addSegueIdentifier(segueIdentifier)
    
    for controller in root.findall(".//*[@storyboardIdentifier]"):
        controllerIdentifier = controller.get("storyboardIdentifier")
        if controllerIdentifier == None:
            continue
        addControllerIdentifier(controllerIdentifier)
    
    for tableViewCell in root.iter("tableViewCell"):
        tableViewCellIdentifier = tableViewCell.get("reuseIdentifier")
        if tableViewCellIdentifier == None:
            continue
        addCellIdentifier(tableViewCellIdentifier)
    
    for collectionViewCell in root.iter("collectionViewCell"):
        collectionViewCellIdentifier = collectionViewCell.get("reuseIdentifier")
        if collectionViewCellIdentifier == None:
            continue
        addCellIdentifier(collectionViewCellIdentifier)


def writeHeader(file, identifiers):
    constants = sorted(identifiers.keys())
    
    for constantName in constants:
        file.write("extern NSString * const " + constantName + ";\n")

def writeImplementation(file, identifiers):
    constants = sorted(identifiers.keys())
    
    for constantName in constants:
        file.write("NSString * const " + constantName + " = @\"" + identifiers[constantName] + "\";\n")

count = os.environ["SCRIPT_INPUT_FILE_COUNT"]
for n in range(int(count)):
    process_storyboard(os.environ["SCRIPT_INPUT_FILE_" + str(n)])

with open(sys.argv[1], "w+") as header:
    header.write("/* Generated document. DO NOT CHANGE */\n\n")
    header.write("/* Segue identifier constants */\n")
    
    writeHeader(header, segueIdentifiers)
    
    header.write("\n")
    header.write("/* Controller identifier constants */\n")
    
    writeHeader(header, controllerIdentifiers)
    
    header.write("\n")
    header.write("/* Cell identifier constants */\n")
    
    writeHeader(header, cellIdentifiers)
    
    header.close()

with open(sys.argv[2], "w+") as implementation:
    implementation.write("/* Generated document. DO NOT CHANGE */\n\n")
    
    writeImplementation(implementation, segueIdentifiers)
    implementation.write("\n")
    
    writeImplementation(implementation, controllerIdentifiers)
    implementation.write("\n")
    
    writeImplementation(implementation, cellIdentifiers)
    
    implementation.close()


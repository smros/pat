#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="steve"
__date__ ="$16-Feb-2012 10:42:38 AM$"

import sqlite
import datetime

class projectStoriesDB(sqlliteDB):

    def createProjectStoriesDB(self):
        tableInit="""

            drop table if exists quotes;

            create table projectStories(
                project TEXT,
                story TEXT,
                owner TEXT,
                startTime DATETIME,
                endTime DATETIME,
                duration FLOAT,
                primary key (project, story, owner, startTime)
                );

            create index idx1 on projectStories(
                project,
                story,
                owner,
                startTime
                );

            """

        self.executeScript(tableInit)
        self.closeDB()

    def insertEvent(self, message):
        # Build the sql trasaction here and run the insert
        prefix = ''' insert or ignore into quotes values (?,?,?,?,?)'''
        dataTuple=(message.project_id,
        message.story_id,
        message.owner,
        message.locEnd,
        datetime.datetime.now().isoformat('-')
        )

#        print prefix
#        print dataTuple

        self.executeTransaction2(prefix, dataTuple)

    def getQuotesFromBook(self, bookTitle):
        prefix = ''' select content from quotes where title = ?'''
        data=self.executeQueryFetchAll2(prefix, bookTitle)
        return(data)

    def getTitlesFromDB(self):
        prefix = ''' select distinct title from quotes'''
        data=self.executeQueryFetchAll(prefix)
        return(data)



if __name__ == "__main__":

    q=quotesDB('agileZenStories.db')
    #q.createQuotesDB()

    
 


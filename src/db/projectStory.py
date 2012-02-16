#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="steve"
__date__ ="$16-Feb-2012 10:42:38 AM$"

from sqllite import sqlliteDB
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

    def getEvent(self, projectID=None, storyID=None, owner=None, startTime=None):
        prefix = ''' select endTime from projectStories where project = ? and story = ? and owner = ? and startTime = ? '''
        data=self.executeQueryFetchAll2(prefix, (projectID, storyID, owner, startTime ) )
        return(data)

    def getTitlesFromDB(self):
        prefix = ''' select distinct title from quotes'''
        data=self.executeQueryFetchAll(prefix)
        return(data)



if __name__ == "__main__":

    q=projectStoriesDB('agileZenStories.db')
    #q.createProjectStoriesDB()
    data=q.getEvent('12345', '1', 'steve','2008-01-01-12:00:00')
    print data
    data=q.getEvent('99999', '3', 'johnny','1999-01-01-12:00:00')
    print data
    data=q.getEvent('99999', '3', 'johnny','1999-01-01-12:01:00')
    print data
    
    q.closeDB()


    #q.createQuotesDB()


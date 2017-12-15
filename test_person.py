#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 08:09:10 2017

@author: ismailnabeel
"""

""" Test Person
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-12-09
:Copyright: 2017, Arthur Goldberg
:License: MIT
"""
import unittest

from person import Person, Gender, PersonError


class TestGender(unittest.TestCase):

    def test_gender(self):
        self.assertEqual(Gender().get_gender('Male'), Gender.MALE)
        self.assertEqual(Gender().get_gender('female'), Gender.FEMALE)
        self.assertEqual(Gender().get_gender('FEMALE'), Gender.FEMALE)
        self.assertEqual(Gender().get_gender('NA'), Gender.UNKNOWN)

        with self.assertRaises(PersonError) as context:
            Gender().get_gender('---')
        self.assertIn('Illegal gender', str(context.exception))


class TestPerson(unittest.TestCase):

    def setUp(self):
        # create a few Persons
        self.child = Person('kid', 'NA')
        self.mom = Person('mom', 'f')
        self.dad = Person('dad', 'm')

        # make a deep family history
        
        self.generations = 4
        self.people = people = []
        self.root_child = Person('root_child', Gender.UNKNOWN)
        people.append(self.root_child)
        def add_parents(child, depth, max_depth):
            if depth+1 < max_depth:
                dad = Person(child.name + '_dad', Gender.MALE)
                mom = Person(child.name + '_mom', Gender.FEMALE)
                people.append(dad)
                people.append(mom)
                child.set_father(dad)
                child.set_mother(mom)
                add_parents(dad, depth+1, max_depth)
                add_parents(mom, depth+1, max_depth)
        add_parents(self.root_child, 0, self.generations)


    def test_set_mother(self):
        '''Testing set_mother'''
        
        self.child.set_mother(self.mom)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)

        self.mom.gender = Gender.MALE
        with self.assertRaises(PersonError) as context:
            self.child.set_mother(self.mom)
        self.assertIn('is not female', str(context.exception))
        
    def test_set_father(self):
        '''Testing set_father'''
        
        self.child.set_father(self.dad)
        self.assertEqual(self.child.father, self.dad)
        self.assertIn(self.child, self.dad.children)

        self.dad.gender = Gender.FEMALE
        with self.assertRaises(PersonError) as context:
            self.child.set_father(self.dad)
        self.assertIn('is not male', str(context.exception))
        
    def test_remove_father(self):
        '''Testing remove_father'''
        
        self.child.set_father(self.dad)
        self.child.remove_father()
        self.assertNotEqual(self.dad,self.child.father)
        self.assertNotIn(self.child, self.dad.children)
        
    def test_remove_mother(self):
        '''Testing remove_mother'''
        
        self.child.set_mother(self.mom)
        self.child.remove_mother()
        self.assertNotEqual(self.mom, self.child.mother)
        self.assertNotIn(self.child, self.mom.children)
        

    
    def test_add_child(self):
        ''' Testing add_child '''
        
        self.assertNotIn(self.child, self.mom.children)
        self.mom.add_child(self.child)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)
        self.assertNotIn(self.child, self.dad.children)
        self.dad.add_child(self.child)
        self.assertEqual(self.child.father, self.dad)
        self.assertIn(self.child, self.dad.children)
        
        
    
    def test_add_child_error(self):
        ''' Test add_child_error '''
        
        self.dad.gender = Gender.UNKNOWN
        with self.assertRaises(PersonError) as context:
            self.dad.add_child(self.child)
        self.assertIn('cannot add child', str(context.exception))    # added the str to test
        self.assertIn('with unknown gender', str(context.exception)) # added the str to test
     
    
    '''def test_remove_father(self):
        self.child.set_father(self.dad)
        self.child.remove_father()
        self.assertNotIn(self.child, self.dad.children)
     '''   
    def test_get_persons_name(self):
        '''Testing get_persons_name '''
        
        self.assertEqual('root_child', self.root_child.get_persons_name(self.root_child))
        self.assertEqual(Person.get_persons_name(self.child),self.child.name)
        self.assertEqual(Person.get_persons_name(None), 'NA')
        self.assertIs(Person.get_persons_name(self.child),self.child.name)
    
    def test_grandparents(self):
        '''Testing grandparents '''
        
        self.assertIn(self.root_child.father.father, self.root_child.grandparents())
        self.assertIn(self.root_child.mother.mother,self.root_child.grandparents())
    
    def test_all_grandparents(self):  
        ''' Testing all_grandparents '''
        
        self.assertIn(self.root_child.father.father.father, self.root_child.all_grandparents())
        self.assertIn(self.root_child.father.father.mother, self.root_child.all_grandparents())
        
        self.assertIn(self.root_child.father.mother.father, self.root_child.all_grandparents())
        self.assertIn(self.root_child.father.mother.father, self.root_child.all_grandparents())
        
        self.assertIn(self.root_child.mother.mother.mother, self.root_child.all_grandparents())
        self.assertIn(self.root_child.mother.mother.father, self.root_child.all_grandparents())
        self.assertIn(self.root_child.mother.father.father, self.root_child.all_grandparents())
        self.assertIn(self.root_child.mother.father.mother, self.root_child.all_grandparents()) 
        
        self.assertIn(self.root_child.mother.father.father, self.root_child.all_grandparents())
        self.assertIsNot(self.root_child.mother.father.father,self.root_child.all_grandparents())
        self.assertIsNotNone(self.root_child.mother.father.father,self.root_child.all_grandparents())
        self.assertIsNot(self.root_child,self.root_child.all_grandparents())
        self.assertIn(self.root_child.mother.mother.mother, self.root_child.all_grandparents())
    
    def test_all_ancestors(self):
        ''' Testing all_ancestors '''
        
        self.assertNotEquals(self.root_child.father,self.root_child.all_ancestors())
        self.assertIn(self.root_child.father.father.father, self.root_child.all_ancestors())
        self.assertIn(self.root_child.mother.mother.mother, self.root_child.all_ancestors())
        self.assertIn(self.root_child.father.mother.mother, self.root_child.all_ancestors())
        self.assertIn(self.root_child.mother.father.mother, self.root_child.all_ancestors())
        
        self.assertIn(self.root_child.father, self.root_child.all_ancestors())
        self.assertIn(self.root_child.father.father,self.root_child.all_ancestors())
        self.assertNotIn(self.root_child,self.root_child.all_ancestors())
        self.assertIn(self.root_child.mother.mother.mother, self.root_child.all_ancestors())
    
    def test_ancestors(self):        
        ''' Testing ancestors '''
        
        self.assertIn(self.root_child.father,self.root_child.ancestors(1))
        self.assertIn(self.root_child.father.father,self.root_child.ancestors(2))
        self.assertIn(self.root_child.father.father.father,self.root_child.ancestors(3))

        self.assertIn(self.root_child.mother.mother.mother,self.root_child.ancestors(3))
        self.assertIn(self.root_child.father.mother,self.root_child.ancestors(2))
        self.assertIn(self.root_child.father.mother.father,self.root_child.ancestors(3))
        
        self.assertIn(self.root_child.mother,self.root_child.ancestors(1))
        self.assertIn(self.root_child.mother.mother,self.root_child.ancestors(2))
        self.assertIn(self.root_child.mother.mother.mother,self.root_child.ancestors(3))
        #self.assertIn(self.root_child.father.father.father.father,self.root_child.ancestors(4)) # not present
        self.assertNotIn(self.root_child.father,self.root_child.ancestors(0))    
        
        with self.assertRaises(PersonError) as context:
            self.root_child.ancestors(min_depth = 2, max_depth = 1)
        self.assertIn('max_depth (1) cannot be less than min_depth (2)', str(context.exception))
        

if __name__ == '__main__':
    unittest.main()

# 

from pages.checkboxes_page import CheckboxesPage


def test_initial_state(checkboxes_pom: CheckboxesPage):
    (checkboxes_pom
     .expect_first_unchecked()
     .expect_second_checked())
    
def test_check_first(checkboxes_pom: CheckboxesPage):
    (checkboxes_pom
     .check_first()
     .expect_first_checked())
    
def test_uncheck_second(checkboxes_pom: CheckboxesPage):
    (checkboxes_pom
     .uncheck_second()
     .expect_second_unchecked())
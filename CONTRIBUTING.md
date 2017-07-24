Contributing Guidelines
=======================

In General
----------

- `PEP 8`.
- Tests, always. Write docs for new features.
- Readable and simple code.
- ReStracturedText in docs.

In Particular
-------------

Questions, Feature Requests, Bug Reports, and Feedback. . .
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

. . .should all be reported on the `Github Issue Tracker`_ .

Setting Up for Local Development
++++++++++++++++++++++++++++++++

1. Fork ebayapi_ on Github. ::

    $ git clone https://github.com/itayazolay/ebayapi.git
    $ cd ebayapi

2. Install development requirements. It is highly recommended that you use a virtualenv. ::

    # After activating your virtualenv
    $ pip install -r requirements.txt


Git Branch Structure
++++++++++++++++++++

ebayapi abides by the following branching model:


``master``
    Latest stable branch. **New features should branch off here**.

``X-issue-name``
    Your branch regarding the new issue.

**Always make a new branch for your work**, no matter how small. Also, **do not put unrelated changes in the same branch or pull request**. This makes it more difficult to merge your changes.

Pull Requests
++++++++++++++

1. Create a new local branch.
::

    # For a new feature
    $ git checkout -b X-issue-name master
    
2. Commit your changes. Write good commit messages.
::

    $ git commit -m "Detailed commit message"
    $ git push origin X-issue-name

3. Before submitting a pull request, check the following:

- If the pull request adds functionality, it is tested and the docs are updated.
- You've added yourself to ``AUTHORS.rst``.

4. Submit a pull request to ``ebayapi:master`` or the appropriate maintenance branch.

Running Tests
+++++++++++++

To run all tests: ::

    $ invoke test

To run tests on Python 2.7, 3.4, 3.5, and 3.6 virtual environments (must have each interpreter installed): ::

    $ tox

Documentation
+++++++++++++

Contributions to the documentation are welcome. Documentation is written in `reStructured Text`_ (rST). A quick rST reference can be found `here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_. Builds are powered by Sphinx_.

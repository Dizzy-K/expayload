Paul Buonopane <paul@namepros.com> at [NamePros](https://www.namepros.com/)  
PGP: https://keybase.io/zenexer  

*I'm working on cleaning up this advisory so that it's more informative at a glance.  Suggestions are welcome.*

This advisory addresses the underlying PHP vulnerabilities behind Dawid Golunski's [CVE-2016-10033][CVE-2016-10033], [CVE-2016-10045][CVE-2016-10045], and [CVE-2016-10074][CVE-2016-10074].  It assumes prior understanding of these vulnerabilities.

This advisory does not yet have associated CVE identifiers.

# Summary #

1. It's impossible to write a universal shell escaping function, for a variety of reasons.  However, PHP attempts to provide two shell escaping functions: escapeshellarg and escapeshellcmd.
2. escapeshellcmd undermines any prior sanitization.  If escapeshellarg($input) would be sufficient in a given environment, escapeshellcmd(escapeshellarg($input)) voids any security guarantees.  This is adequately demonstrated in the PoC for [CVE-2016-10045][CVE-2016-10045].
3. PHP uses escapeshellcmd internally.  For example, $additional_parameters in the mail function is passed through escapeshellcmd.  This leads to the same vulnerability as #2, but it can happen even if escapeshellcmd never appears directly in an application's code.  This makes it more difficult for developers to determine if their applications are vulnerable.

# Vulnerabilities #

1. php_escape_shell_cmd, the C function behind escapeshellcmd, is an "inherently dangerous function" because it can never fulfill the security guarantees it attempts to provide.  This vulnerability specifically addresses PHP's own internal use of php_escape_shell_cmd, not its exposure to PHP code via escapeshellcmd.
2. popen, exec, shell_exec, system, passthru, proc_open, and mail can potentially receive user input.  A cautious developer would think to first sanitize this input before passing it to the affected functions.  However, all of those functions are environment-dependent in such a way that sanitization cannot reasonably be performed.  This would not be an issue if secure alternatives, such as pcntl_exec, were universally available.  (Additionally note that some PHP implementations, such as HHVM, don't offer pcntl_fork/pcntl_exec at all.  That may seem out-of-scope, but those implementations rely on vanilla PHP for their design.)
3. escapeshellarg and escapeshellcmd don't properly sanitize input in the context of many Windows applications.  [Here's why.](http://daviddeley.com/autohotkey/parameters/parameters.htm#WINPASS)  This issue made [a previous appearance on bugs.php.net in 2009](https://bugs.php.net/bug.php?id=49446).  This issue cannot be fully resolved by improving escapeshellarg because it is impossible to enumerate all possibilities.  Any program has the freedom to introduce its own parsing rules.
4. escapeshellarg and escapeshellcmd may fail to properly sanitize input when a shell other than sh or bash is used.  This issue (made a previous appearance on bugs.php.net in 2012](https://bugs.php.net/bug.php?id=61706).  This issue cannot be fully resolved by improving escapeshellarg because it is infeasible to maintain rules for all possible shells.
5. escapeshellarg and escapeshellcmd assume that all encodings involved--particularly that of the shell--are ASCII-compatible.  This is not always the case.  Take EUC, for example, which is a stateful encoding.  Stateful encodings in particular are likely to be mangled.  Of all the vulnerabilities listed, I'm least certain of the current impact of this one; it could be vast or negligible.
6. escapeshellarg and escapeshellcmd do not and cannot reasonably provide the security that they attempt to guarantee.  Unlike vuln 1, which handles PHP's own internal use of these functions, this vulnerability addresses the fact that PHP exposes these functions to developers writing PHP code.  Developers use these functions expecting that they will provide bulletproof sanitization, when, in fact, they can't.

## CVE categorization ##

Numbered to match detailed descriptions above.

* CWE-242: Use of Inherently Dangerous Function
    * (1) php_escape_shell_cmd is used internally by several PHP functions, and even more when safe_mode is enabled.  It can never fulfill the security promise it attempts to make.
* CWE-439: Behavioral Change in New Version or Environment
    * (2) popen, exec, shell_exec, system, passthru, proc_open, and mail cannot receive user input for at least one argument, as their behavior is environment-dependent, and escaping is infeasible.  This would not be an issue if secure alternatives, such as pcntl_exec, were universally available.
* CWE-75: Failure to Sanitize Special Elements into a Different Plane (Special Element Injection)
    * (3) escapeshellarg and escapeshellcmd fail to neutralize special elements in the context of many Windows applications.
    * (4) escapeshellarg and escapeshellcmd may fail to neutralize special elements in the context of shells other than sh and bash on POSIX platforms.
* CWE-838: Inappropriate Encoding for Output Context
    * (5) escapeshellarg and escapeshellcmd may behave incorrectly when the current encoding of PHP, the script, or the shell is not ASCII-compatible (e.g., stateful encodings).
* CWE-684: Incorrect Provision of Specified Functionality
    * (6) escapeshellarg and escapeshellcmd do not and cannot reasonably provide the security that they attempt to guarantee.

# Testing #

As of writing, [this utility](https://gist.github.com/Zenexer/c123604d57914970ac297413751c3f21) provides an accurate representation of PHP's escapeshell functions on Linux and Windows.  It was released hastily and isn't designed to be a long-term testing solution.

# Shell escaping #

On Windows, the shell doesn't handle command line parsing; [the target program does](http://daviddeley.com/autohotkey/parameters/parameters.htm#WINPASS).  Different technologies adhere to different algorithms when parsing arguments.  As such, it's not possible to write a universal escape function that works on Windows.

On POSIX systems such as Linux, Mac, and BSD, the shell handles command line parsing.  However, the user typically has control over the shells available on their system, and different distros often favor different shells.  escapeshellarg and escapeshellcmd are designed for sh and bash; using them with other shells means that input may be improperly escaped.  It's not reasonable to write a shell escape function that handles all possible shells.

On any platform, character encoding can play a part in how arguments are interpreted, particularly when non-ASCII-compatible encodings are used.  This isn't likely to be an issue in regions that use Latin-based alphabets, but in other parts of the world, the current escape functions could have unpredictable results.

# Interim solution #

Application developers will need to avoid using escapeshellarg and escapeshellcmd to sanitize user input.  Even if input was already sanitized, once passed through those functions, it should be considered dirty.  This makes certain parameters of certain built-in functions (e.g., $additional_parameters of mail) incapable of securely handling user input securely.

Safe mode must be disabled.

PHP should not be run on Windows in production environments, or where input or code can be affected by third parties.  Under no circumstances are escapeshellarg or escapeshellcmd remotely secure on Windows, and applications that rely on them for security will be vulnerable.

Developer should prefer pcntl_fork + pcntl_exec over alternatives that pass commands through the shell.  Unfortunately, these functions aren't available in many environments, such as HHVM.

If shell escaping absolutely must be applied to user input, be sure to check that the shell and encoding are what you expect them to be.  As a general rule, on POSIX, UTF-8 and sh/bash should be safe with escapeshellarg.  On Windows, escaping will need to be customized for each executable.

escapeshellcmd should be considered inherently dangerous and shouldn't be used for escaping under any circumstances.  Functions that use it internally, such as mail, will need to be handled with care.

## Sanitizing input for safe shell parsing ##

A proper utility will eventually land here: https://github.com/Zenexer/safeshell

In the meantime, the following code block is written by me and in the public domain, per [CC0](https://creativecommons.org/publicdomain/zero/1.0/).  There's also a more advanced version combining the techniques in a separate file below, but it hasn't been thoroughly tested yet.

``` php
/**
 * Prevent attacks similar to CVE-2016-10033, CVE-2016-10045, and CVE-2016-10074
 * by disallowing potentially unsafe shell characters.
 *
 * @param   string  $string      the string to be tested for shell safety
 * @see     https://gist.github.com/Zenexer/40d02da5e07f151adeaeeaa11af9ab36
 * @author  Paul Buonopane <paul@namepros.com>
 * @license Public doman per CC0 1.0.  Attribution appreciated but not required.
 */
function isShellSafe($string)
{
    $string = strval($string);
    $length = strlen($string);

    // If you need to allow empty strings, you can remove this, but be sure you
    // understand the security implications of doing so.
    if (!$length) {
        return false;
    }

    // Method 1
    // Note: Results may be indeterminate with a stateful encodings, e.g. EUC
    for ($i = 0; $i < $length; $i++) {
        $c = $string[$i];
        if (!ctype_alnum($c) && strpos('@_-.', $c) === false) {
            return false;
        }
    }
    //return true;

    // Method 2
    // Note: Assumes UTF-8 encoding.  Conversion may be necessary.
    return (bool) preg_match('/\A[\pL\pN._@-]*\z/ui', $string);
}
```

# Long-term solution #

PHP functions that rely on escapeshellcmd, such as mail, will need to be redesigned to take arrays of arguments and avoid using the shell.

PHP functions that rely on the shell, such as popen and exec, will need to be replaced with functions that take arrays of arguments and avoid using the shell (e.g., fork + execve).  This behavior already exists in the form of pcntl_fork + pcntl_exec, but pcntl isn't as widely supported as popen and exec.

# Public disclosure #

Before this document was published, it was clear that the probability of this information already being known by malicious parties was high.  With an increased chance in widespread attacks following the attention CVE-2016-10033 and CVE-2016-10045, priority was placed on distributing the advisory as quickly and efficiently as possible.

# Affected projects #

* CodeIgniter
* Drupal
* Joomla!
* PHPMailer
* Swift Mailer
* WordPress

[CVE-2016-10033]: https://legalhackers.com/advisories/PHPMailer-Exploit-Remote-Code-Exec-CVE-2016-10033-Vuln.html "Advisory from Dawid Golunski on CVE-2016-10033"
[CVE-2016-10045]: https://legalhackers.com/advisories/PHPMailer-Exploit-Remote-Code-Exec-CVE-2016-10045-Vuln-Patch-Bypass.html "Advisory from Dawid Golunski on CVE-2016-10045"
[CVE-2016-10074]: https://legalhackers.com/advisories/SwiftMailer-Exploit-Remote-Code-Exec-CVE-2016-10074-Vuln.html "Advisory from Dawid Golunski on CVE-2016-10074"
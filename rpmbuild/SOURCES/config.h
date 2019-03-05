/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will frequently occur because arch-specific build-time
 * configuration options are stored (and used, so they can't just be stripped
 * out) in config.h.  The original config.h has been renamed.
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifdef srtp_multilib_redirection_h
#error "Do not define srtp_multilib_redirection_h!"
#endif
#define srtp_multilib_redirection_h

#if defined(__x86_64__) || defined(__PPC64__) || (defined(__sparc__) && defined(__arch64__)) || defined(__s390x__) || defined(__aarch64__)
#include "srtp/config-64.h"
#else
#include "srtp/config-32.h"
#endif

#undef srtp_multilib_redirection_h

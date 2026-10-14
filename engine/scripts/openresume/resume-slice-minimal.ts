// Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
// Minimal stand-in for lib/redux/resumeSlice, to run the OpenResume parser without installing
// Redux. The parser only uses this constant (value copied from the original).
export const initialFeaturedSkills = Array(6).fill({ skill: "", rating: 4 });
